"""FastAPI 서버 (다국어 지원).

엔드포인트:
- GET  /health
- GET  /api/ui?lang=ko|en        : 화면 라벨 (언어별)
- GET  /api/contents?lang=        : 콘텐츠 목록 (F1)
- GET  /api/route/{cid}?lang=     : 동선 + 지점별 해설·체험·방문정보 (F2·F3·F4)
- POST /api/ask                   : 질문 응답 (F5, 선택 언어로)
- GET  /                          : 프론트엔드
"""
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .llm import answer_question

BASE = Path(__file__).resolve().parent.parent
DATA = json.loads((BASE / "data" / "contents.json").read_text(encoding="utf-8"))

PLACES = {p["place_id"]: p for p in DATA["places"]}
ROUTE_BY_CONTENT = {r["content_id"]: r for r in DATA["routes"]}
LANGS = DATA.get("languages", ["ko"])


def loc(value, lang):
    """{ko,en} 묶음이면 해당 언어를 고르고(없으면 ko), 아니면 그대로 반환."""
    if isinstance(value, dict) and ("ko" in value or "en" in value):
        return value.get(lang) or value.get("ko") or ""
    return value


def pick_lang(lang: str) -> str:
    return lang if lang in LANGS else "ko"


app = FastAPI(title="서울 스토리 동선 추천 AI봇")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/ui")
def ui_labels(lang: str = "ko"):
    """화면에 쓰이는 라벨 묶음(언어별)."""
    lang = pick_lang(lang)
    return {"lang": lang, "langs": LANGS, "labels": DATA["ui"].get(lang, DATA["ui"]["ko"])}


@app.get("/api/contents")
def list_contents(lang: str = "ko"):
    """F1: 콘텐츠 목록 (선택 언어)."""
    lang = pick_lang(lang)
    return [{"content_id": c["content_id"], "title": loc(c["title"], lang),
             "summary": loc(c["summary"], lang)} for c in DATA["contents"]]


@app.get("/api/route/{content_id}")
def get_route(content_id: str, lang: str = "ko"):
    """F2·F3·F4: 동선 + 지점별 정보 (선택 언어)."""
    lang = pick_lang(lang)
    route = ROUTE_BY_CONTENT.get(content_id)
    if not route:
        raise HTTPException(status_code=404, detail="해당 콘텐츠의 동선이 없습니다.")
    stops = []
    for s in sorted(route["stops"], key=lambda x: x["order"]):
        place = PLACES.get(s["place_id"], {})
        stops.append({
            "order": s["order"],
            "stop_type": loc(s["stop_type"], lang),
            "name": loc(place.get("name", ""), lang),
            "area": loc(place.get("area", ""), lang),
            "map_query": place.get("map_query", ""),
            "place_story": loc(place.get("place_story", ""), lang),
            "story_text": loc(s["story_text"], lang),
            "theme_exp": loc(s["theme_exp"], lang),
            "visit": loc(s.get("visit", ""), lang),
        })
    return {"route_id": route["route_id"], "title": loc(route["title"], lang), "stops": stops}


class AskBody(BaseModel):
    content_id: str
    question: str
    lang: str = "ko"


@app.post("/api/ask")
def ask(body: AskBody):
    """F5: 해당 동선의 준비된 텍스트(선택 언어)만 근거로 답한다."""
    lang = pick_lang(body.lang)
    route = ROUTE_BY_CONTENT.get(body.content_id)
    if not route:
        raise HTTPException(status_code=404, detail="해당 콘텐츠의 동선이 없습니다.")
    context = []
    for s in route["stops"]:
        context.append(loc(s["story_text"], lang))
        place = PLACES.get(s["place_id"], {})
        if place.get("place_story"):
            context.append(loc(place["place_story"], lang))
    return {"answer": answer_question(body.question, context, lang)}


app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


@app.get("/")
def index():
    return FileResponse(BASE / "static" / "index.html")
