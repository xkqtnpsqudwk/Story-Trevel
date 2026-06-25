# -*- coding: utf-8 -*-
"""SQLite 데이터 계층 (자동 생성·시드 + 조회).

모든 시드 데이터는 catalog.py 한 곳에서 온다(지역·OTT·연예인·작품·장소).
contents.json은 더 이상 데이터 소스가 아니라 화면 문구(ui) 전용이다.
서버 시작 시 init()이 DB가 비어 있으면 catalog로 시드한다.
"""
import sqlite3

try:
    from . import catalog
except ImportError:
    import catalog

from pathlib import Path
BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / "data" / "app.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS province(
  id TEXT PRIMARY KEY, name_ko TEXT, name_en TEXT, sort INTEGER);
CREATE TABLE IF NOT EXISTS city(
  id TEXT PRIMARY KEY, province_id TEXT, name_ko TEXT, name_en TEXT, sort INTEGER);
CREATE TABLE IF NOT EXISTS platform(
  id TEXT PRIMARY KEY, name_ko TEXT, name_en TEXT, kind TEXT, sort INTEGER);
CREATE TABLE IF NOT EXISTS person(
  id TEXT PRIMARY KEY, name_ko TEXT, name_en TEXT, kind TEXT, sort INTEGER);
CREATE TABLE IF NOT EXISTS work(
  id TEXT PRIMARY KEY, title_ko TEXT, title_en TEXT,
  summary_ko TEXT, summary_en TEXT, popularity INTEGER);
CREATE TABLE IF NOT EXISTS place(
  id TEXT PRIMARY KEY, city_id TEXT, sort INTEGER,
  name_ko TEXT, name_en TEXT, area_ko TEXT, area_en TEXT, map_query TEXT,
  stop_type_ko TEXT, stop_type_en TEXT, visit_ko TEXT, visit_en TEXT,
  theme_ko TEXT, theme_en TEXT, place_story_ko TEXT, place_story_en TEXT);
CREATE TABLE IF NOT EXISTS work_platform(
  work_id TEXT, platform_id TEXT, PRIMARY KEY(work_id, platform_id));
CREATE TABLE IF NOT EXISTS work_person(
  work_id TEXT, person_id TEXT, PRIMARY KEY(work_id, person_id));
CREATE TABLE IF NOT EXISTS place_work(
  place_id TEXT, work_id TEXT, story_ko TEXT, story_en TEXT,
  PRIMARY KEY(place_id, work_id));
"""


def connect(db_path=DB_PATH):
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def seed(conn, cat):
    """비어 있을 때만 시드(idempotent)."""
    cur = conn.cursor()
    if cur.execute("SELECT COUNT(*) FROM work").fetchone()[0] > 0:
        return False
    for i, (pid, ko, en) in enumerate(cat.PROVINCES):
        cur.execute("INSERT INTO province VALUES(?,?,?,?)", (pid, ko, en, i))
    for i, (cid, pid, ko, en) in enumerate(cat.CITIES):
        cur.execute("INSERT INTO city VALUES(?,?,?,?,?)", (cid, pid, ko, en, i))
    for i, (pid, ko, en, kind) in enumerate(cat.PLATFORMS):
        cur.execute("INSERT INTO platform VALUES(?,?,?,?,?)", (pid, ko, en, kind, i))
    for i, (pid, ko, en, kind) in enumerate(cat.PERSONS):
        cur.execute("INSERT INTO person VALUES(?,?,?,?,?)", (pid, ko, en, kind, i))
    # 작품: 원본 6 + 큐레이션 27
    for wid, tko, ten, sko, sen in (cat.BASE_WORKS + cat.CURATED_WORKS):
        cur.execute("INSERT OR IGNORE INTO work VALUES(?,?,?,?,?,?)",
                    (wid, tko, ten, sko, sen, cat.POPULARITY.get(wid, 0)))
    for wid, plats in cat.WORK_PLATFORM.items():
        for plat in plats:
            cur.execute("INSERT OR IGNORE INTO work_platform VALUES(?,?)", (wid, plat))
    for wid, persons in cat.WORK_PERSON.items():
        for per in persons:
            cur.execute("INSERT OR IGNORE INTO work_person VALUES(?,?)", (wid, per))
    # 장소(원본+촬영지) + 작품 해설
    for pl in cat.PLACES:
        cur.execute("INSERT OR IGNORE INTO place VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            pl["place_id"], pl["city"], pl.get("sort", 0),
            pl["name_ko"], pl["name_en"], pl["area_ko"], pl["area_en"], pl["map_query"],
            pl["stop_ko"], pl["stop_en"], pl["visit_ko"], pl["visit_en"],
            pl["theme_ko"], pl["theme_en"], pl["story_ko"], pl["story_en"]))
        for wid, sko, sen in pl["links"]:
            cur.execute("INSERT OR IGNORE INTO place_work VALUES(?,?,?,?)", (pl["place_id"], wid, sko, sen))
    for pid, wid, sko, sen in getattr(cat, "EXTRA_PLACE_WORK", []):
        cur.execute("INSERT OR IGNORE INTO place_work VALUES(?,?,?,?)", (pid, wid, sko, sen))
    conn.commit()
    return True


def init(db_path=DB_PATH):
    conn = connect(db_path)
    conn.executescript(SCHEMA)
    seed(conn, catalog)
    return conn


# ---------- 조회 ----------

def _name(row, lang):
    return row["name_" + ("en" if lang == "en" else "ko")] or row["name_ko"]


def list_provinces(conn, lang="ko"):
    rows = conn.execute("SELECT * FROM province ORDER BY sort").fetchall()
    out = []
    for r in rows:
        has = conn.execute(
            "SELECT 1 FROM city c JOIN place p ON p.city_id=c.id "
            "WHERE c.province_id=? LIMIT 1", (r["id"],)).fetchone() is not None
        out.append({"id": r["id"], "name": _name(r, lang), "has_data": has})
    return out


def list_cities(conn, province_id, lang="ko"):
    rows = conn.execute(
        "SELECT * FROM city WHERE province_id=? ORDER BY sort", (province_id,)).fetchall()
    out = []
    for r in rows:
        has = conn.execute(
            "SELECT 1 FROM place WHERE city_id=? LIMIT 1", (r["id"],)).fetchone() is not None
        out.append({"id": r["id"], "name": _name(r, lang), "has_data": has})
    return out


def list_platforms(conn, city_id, lang="ko"):
    """선택 시에 '동선 있는 작품'을 가진 플랫폼만. count=그 동선 작품 수."""
    rows = conn.execute(
        "SELECT pl.id, pl.name_ko, pl.name_en, pl.kind, "
        "COUNT(DISTINCT pkw.work_id) AS n FROM platform pl "
        "JOIN work_platform wp ON wp.platform_id=pl.id "
        "JOIN place_work pkw ON pkw.work_id=wp.work_id "
        "JOIN place p ON p.id=pkw.place_id AND p.city_id=? "
        "GROUP BY pl.id HAVING n>0 ORDER BY pl.sort", (city_id,)).fetchall()
    return [{"id": r["id"], "name": _name(r, lang), "kind": r["kind"], "count": r["n"]} for r in rows]


def list_persons(conn, city_id, lang="ko"):
    rows = conn.execute(
        "SELECT pe.id, pe.name_ko, pe.name_en, pe.kind, "
        "COUNT(DISTINCT pkw.work_id) AS n FROM person pe "
        "JOIN work_person wp ON wp.person_id=pe.id "
        "JOIN place_work pkw ON pkw.work_id=wp.work_id "
        "JOIN place p ON p.id=pkw.place_id AND p.city_id=? "
        "GROUP BY pe.id HAVING n>0 ORDER BY pe.sort", (city_id,)).fetchall()
    return [{"id": r["id"], "name": _name(r, lang), "kind": r["kind"], "count": r["n"]} for r in rows]


def _has_route(conn, city_id, work_id):
    return conn.execute(
        "SELECT 1 FROM place p JOIN place_work pw ON pw.place_id=p.id "
        "WHERE p.city_id=? AND pw.work_id=? LIMIT 1", (city_id, work_id)).fetchone() is not None


def _works_by(conn, join, col, val, city_id, lang):
    rows = conn.execute(
        f"SELECT DISTINCT w.* FROM work w JOIN {join} j ON j.work_id=w.id "
        f"WHERE j.{col}=? ORDER BY w.popularity DESC", (val,)).fetchall()
    out = []
    for r in rows:
        out.append({
            "work_id": r["id"],
            "title": r["title_en"] if lang == "en" else r["title_ko"],
            "summary": r["summary_en"] if lang == "en" else r["summary_ko"],
            "has_route": _has_route(conn, city_id, r["id"]) if city_id else False,
        })
    out.sort(key=lambda x: 0 if x["has_route"] else 1)
    return out


def works_by_platform(conn, platform_id, city_id, lang="ko"):
    return _works_by(conn, "work_platform", "platform_id", platform_id, city_id, lang)


def works_by_person(conn, person_id, city_id, lang="ko"):
    return _works_by(conn, "work_person", "person_id", person_id, city_id, lang)


def route(conn, city_id, work_id, lang="ko"):
    w = conn.execute("SELECT * FROM work WHERE id=?", (work_id,)).fetchone()
    if not w:
        return None
    rows = conn.execute(
        "SELECT p.*, pw.story_ko, pw.story_en FROM place p "
        "JOIN place_work pw ON pw.place_id=p.id "
        "WHERE p.city_id=? AND pw.work_id=? ORDER BY p.sort", (city_id, work_id)).fetchall()
    stops = []
    for r in rows:
        cross = conn.execute(
            "SELECT w.id, w.title_ko, w.title_en FROM place_work pw "
            "JOIN work w ON w.id=pw.work_id WHERE pw.place_id=? AND pw.work_id<>?",
            (r["id"], work_id)).fetchall()
        stops.append({
            "place_id": r["id"], "name": _name(r, lang),
            "area": r["area_en"] if lang == "en" else r["area_ko"],
            "map_query": r["map_query"],
            "stop_type": r["stop_type_en"] if lang == "en" else r["stop_type_ko"],
            "story_text": r["story_en"] if lang == "en" else r["story_ko"],
            "place_story": r["place_story_en"] if lang == "en" else r["place_story_ko"],
            "theme_exp": r["theme_en"] if lang == "en" else r["theme_ko"],
            "visit": r["visit_en"] if lang == "en" else r["visit_ko"],
            "cross": [{"work_id": c["id"],
                       "title": c["title_en"] if lang == "en" else c["title_ko"]} for c in cross],
        })
    return {"work_id": work_id,
            "work_title": w["title_en"] if lang == "en" else w["title_ko"],
            "stops": stops}


def ask_context(conn, city_id, work_id, lang="ko"):
    r = route(conn, city_id, work_id, lang)
    if not r:
        return []
    ctx = []
    for s in r["stops"]:
        if s["story_text"]:
            ctx.append(s["story_text"])
        if s["place_story"]:
            ctx.append(s["place_story"])
    return ctx
