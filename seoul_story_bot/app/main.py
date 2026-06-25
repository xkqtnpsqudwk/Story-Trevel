"""FastAPI 서버 (DB 기반 · 새 흐름: 도→시→OTT/연예인→작품→동선).

엔드포인트:
- GET  /health
- GET  /api/ui?lang
- GET  /api/provinces?lang                  : 도 목록(데이터 유무)
- GET  /api/cities?province=&lang           : 시 목록(데이터 유무)
- GET  /api/platforms?lang                  : OTT·채널 목록
- GET  /api/persons?lang                    : 연예인 목록
- GET  /api/works?city=&platform=|person=&lang : 작품 목록(인기순, 동선 유무)
- GET  /api/route?city=&work=&lang          : 작품 동선(장소들 + 교차안내)
- POST /api/ask                             : 질문 응답(F5, 동선 근거)
- GET  /                                    : 프론트엔드
"""
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import db
from .llm import answer_question, OUT_OF_SCOPE

BASE = Path(__file__).resolve().parent.parent
UI = json.loads((BASE / "data" / "contents.json").read_text(encoding="utf-8")).get("ui", {})
LANGS = ["ko", "en"]

CONN = db.init()  # DB 없으면 자동 생성·시드


def pick_lang(lang):
    return lang if lang in LANGS else "ko"


app = FastAPI(title="이야기가 있는 여행")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/ui")
def ui(lang: str = "ko"):
    lang = pick_lang(lang)
    return {"lang": lang, "langs": LANGS, "labels": UI.get(lang, UI.get("ko", {}))}


@app.get("/api/provinces")
def provinces(lang: str = "ko"):
    return db.list_provinces(CONN, pick_lang(lang))


@app.get("/api/cities")
def cities(province: str, lang: str = "ko"):
    return db.list_cities(CONN, province, pick_lang(lang))


@app.get("/api/platforms")
def platforms(city: str, lang: str = "ko"):
    return db.list_platforms(CONN, city, pick_lang(lang))


@app.get("/api/persons")
def persons(city: str, lang: str = "ko"):
    return db.list_persons(CONN, city, pick_lang(lang))


@app.get("/api/works")
def works(city: str, lang: str = "ko", platform: str = None, person: str = None):
    lang = pick_lang(lang)
    if platform:
        return db.works_by_platform(CONN, platform, city, lang)
    if person:
        return db.works_by_person(CONN, person, city, lang)
    raise HTTPException(status_code=400, detail="platform 또는 person 파라미터가 필요합니다.")


@app.get("/api/route")
def route(city: str, work: str, lang: str = "ko"):
    r = db.route(CONN, city, work, pick_lang(lang))
    if r is None:
        raise HTTPException(status_code=404, detail="없는 작품입니다.")
    return r  # stops가 비어 있으면 프론트가 '동선 준비 중'으로 표시


class AskBody(BaseModel):
    city: str
    work: str
    question: str
    lang: str = "ko"


@app.post("/api/ask")
def ask(body: AskBody):
    lang = pick_lang(body.lang)
    ctx = db.ask_context(CONN, body.city, body.work, lang)
    if not ctx:  # 동선(근거) 없음 → 범위 밖 안내
        return {"answer": OUT_OF_SCOPE.get(lang, OUT_OF_SCOPE["ko"])}
    return {"answer": answer_question(body.question, ctx, lang)}


app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


@app.get("/")
def index():
    return FileResponse(BASE / "static" / "index.html")
