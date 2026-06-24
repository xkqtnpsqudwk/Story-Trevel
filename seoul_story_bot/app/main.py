"""FastAPI 서버 (데모).

엔드포인트:
- GET  /health            : 서버 동작 확인
- GET  /api/contents      : 콘텐츠 목록 (F1)
- GET  /api/route/{cid}   : 콘텐츠의 동선 + 지점별 해설·체험 (F2·F3·F4)
- POST /api/ask           : 질문 응답 (F5, 준비된 텍스트 근거)
- GET  /                  : 프론트엔드(static/index.html)
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

# id로 빠르게 찾기 위한 인덱스 (정보 장부의 색인 같은 것)
PLACES = {p["place_id"]: p for p in DATA["places"]}
ROUTE_BY_CONTENT = {r["content_id"]: r for r in DATA["routes"]}

app = FastAPI(title="서울 스토리 동선 추천 AI봇")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/contents")
def list_contents():
    """F1: 사용자가 고를 콘텐츠 목록."""
    return DATA["contents"]


@app.get("/api/route/{content_id}")
def get_route(content_id: str):
    """F2·F3·F4: 콘텐츠에 연결된 동선과 지점별 해설·체험."""
    route = ROUTE_BY_CONTENT.get(content_id)
    if not route:
        raise HTTPException(status_code=404, detail="해당 콘텐츠의 동선이 없습니다.")
    # 각 지점에 장소 정보(이름·위치·장소 이야기)를 합쳐서 내려준다
    stops = []
    for s in sorted(route["stops"], key=lambda x: x["order"]):
        place = PLACES.get(s["place_id"], {})
        stops.append({
            "order": s["order"],
            "stop_type": s["stop_type"],
            "name": place.get("name", ""),
            "area": place.get("area", ""),
            "map_query": place.get("map_query", place.get("name", "")),
            "place_story": place.get("place_story", ""),
            "story_text": s["story_text"],   # 드라마 ↔ 장소 연결 해설 (F3)
            "theme_exp": s["theme_exp"],     # 주변 테마 체험 (F4)
        })
    return {"route_id": route["route_id"], "title": route["title"], "stops": stops}


class AskBody(BaseModel):
    content_id: str
    question: str


@app.post("/api/ask")
def ask(body: AskBody):
    """F5: 해당 동선의 준비된 텍스트만 근거로 답한다."""
    route = ROUTE_BY_CONTENT.get(body.content_id)
    if not route:
        raise HTTPException(status_code=404, detail="해당 콘텐츠의 동선이 없습니다.")
    # 근거 = 이 동선의 모든 story_text + 각 장소의 place_story
    context = []
    for s in route["stops"]:
        context.append(s["story_text"])
        place = PLACES.get(s["place_id"], {})
        if place.get("place_story"):
            context.append(place["place_story"])
    return {"answer": answer_question(body.question, context)}


# 프론트엔드 정적 파일 서빙
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


@app.get("/")
def index():
    return FileResponse(BASE / "static" / "index.html")
