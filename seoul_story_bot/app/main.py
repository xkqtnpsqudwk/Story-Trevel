"""FastAPI 서버 (권역 모델 · 다국어).

모델: 하나의 권역(종로·북촌) 안 장소들에 콘텐츠를 다대다로 태그.
콘텐츠를 고르면 = 그 콘텐츠가 태그된 권역 장소들을 도보 동선으로 제시.

엔드포인트:
- GET  /health
- GET  /api/ui?lang=          : 화면 라벨
- GET  /api/contents?lang=    : 콘텐츠 목록 (태그된 것만) (F1)
- GET  /api/route/{cid}?lang= : 권역 동선 = 콘텐츠 태그된 장소들 + 교차 안내 (F2·F3·F4)
- POST /api/ask               : 질문 응답 (F5, 선택 콘텐츠 근거)
- GET  /                      : 프론트엔드
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
PLACES = sorted(DATA["places"], key=lambda p: p.get("order", 0))
CONTENTS = {c["content_id"]: c for c in DATA["contents"]}
LANGS = DATA.get("languages", ["ko"])


def loc(v, lang):
    if isinstance(v, dict) and ("ko" in v or "en" in v):
        return v.get(lang) or v.get("ko") or ""
    return v


def pick_lang(lang):
    return lang if lang in LANGS else "ko"


def places_for(content_id):
    """해당 콘텐츠가 태그된 권역 장소들(순서대로)."""
    return [p for p in PLACES if content_id in p.get("contents", {})]


app = FastAPI(title="서울 권역 스토리 동선 AI봇")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/ui")
def ui_labels(lang: str = "ko"):
    lang = pick_lang(lang)
    return {"lang": lang, "langs": LANGS, "labels": DATA["ui"].get(lang, DATA["ui"]["ko"])}


@app.get("/api/contents")
def list_contents(lang: str = "ko"):
    """F1: 권역에 태그된 콘텐츠만 목록으로."""
    lang = pick_lang(lang)
    tagged = {cid for p in PLACES for cid in p.get("contents", {})}
    out = []
    for c in DATA["contents"]:
        if c["content_id"] in tagged:
            out.append({"content_id": c["content_id"], "title": loc(c["title"], lang),
                        "summary": loc(c["summary"], lang),
                        "place_count": len(places_for(c["content_id"]))})
    return out


@app.get("/api/route/{content_id}")
def get_route(content_id: str, lang: str = "ko"):
    """F2·F3·F4: 콘텐츠가 태그된 권역 장소들 + 장소별 교차 안내."""
    lang = pick_lang(lang)
    if content_id not in CONTENTS:
        raise HTTPException(status_code=404, detail="없는 콘텐츠입니다.")
    tagged = places_for(content_id)
    if not tagged:
        raise HTTPException(status_code=404, detail="이 콘텐츠로 연결된 장소가 없습니다.")
    stops = []
    for p in tagged:
        link = p["contents"][content_id]
        # 교차 안내: 같은 장소의 다른 콘텐츠 태그
        cross = [{"content_id": cid, "title": loc(CONTENTS[cid]["title"], lang)}
                 for cid in p["contents"] if cid != content_id and cid in CONTENTS]
        stops.append({
            "place_id": p["place_id"],
            "name": loc(p["name"], lang),
            "area": loc(p["area"], lang),
            "map_query": p.get("map_query", ""),
            "stop_type": loc(p["stop_type"], lang),
            "story_text": loc(link["story_text"], lang),
            "place_story": loc(p.get("place_story", ""), lang),
            "theme_exp": loc(p.get("theme_exp", ""), lang),
            "visit": loc(p.get("visit", ""), lang),
            "cross": cross,
        })
    return {
        "content_id": content_id,
        "content_title": loc(CONTENTS[content_id]["title"], lang),
        "area_name": loc(DATA["area"]["name"], lang),
        "area_blurb": loc(DATA["area"]["blurb"], lang),
        "stops": stops,
    }


class AskBody(BaseModel):
    content_id: str
    question: str
    lang: str = "ko"


@app.post("/api/ask")
def ask(body: AskBody):
    """F5: 선택 콘텐츠로 태그된 장소들의 준비 텍스트만 근거로 답한다."""
    lang = pick_lang(body.lang)
    tagged = places_for(body.content_id)
    if not tagged:
        raise HTTPException(status_code=404, detail="이 콘텐츠로 연결된 장소가 없습니다.")
    context = []
    for p in tagged:
        context.append(loc(p["contents"][body.content_id]["story_text"], lang))
        if p.get("place_story"):
            context.append(loc(p["place_story"], lang))
    return {"answer": answer_question(body.question, context, lang)}


app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


@app.get("/")
def index():
    return FileResponse(BASE / "static" / "index.html")
