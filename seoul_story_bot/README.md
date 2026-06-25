# 이야기가 있는 여행 (Travel with Stories)

좋아하는 K-콘텐츠를 **OTT·연예인**으로 고르면, 그 작품의 **실제 서울 촬영지**를
도보 동선으로 묶어 '콘텐츠 장면 ↔ 장소 이야기'로 안내하는 웹 서비스.
타깃은 외국인 관광객이며 한국어/영어를 지원한다.

## 화면 흐름
도(전국) → 시·구 → **OTT** 또는 **연예인** → 작품 → 동선(장소별 지도·해설·교차안내) → 질문(AI)

- 동선이 있는 작품이 먼저, 아직 장소가 없는 작품은 '동선 준비 중'으로 표시.
- OTT·연예인 목록에는 선택한 시에 **동선이 있는 작품 수**만 표시(없으면 숨김).

## 기술 스택
- 백엔드: FastAPI (Python)
- DB: SQLite — 서버 시작 시 자동 생성·시드 (별도 설치 없음)
- 프론트엔드: 정적 HTML + 바닐라 JS (웹/모바일 별도 레이아웃, 폭 1000px 기준)
- AI(질문 응답): 로컬 Ollama 기본(요금 없음), OpenAI로도 전환 가능

## 폴더 구조
```
seoul_story_bot/
├─ app/
│  ├─ main.py     # FastAPI 라우트
│  ├─ db.py       # SQLite 생성·시드·조회
│  ├─ catalog.py  # 시드 데이터 단일 소스(지역·OTT·연예인·작품·장소)
│  └─ llm.py      # 질문 응답(AI, 근거 주입)
├─ data/
│  ├─ contents.json # 화면 문구(ui) 전용 — 데이터 아님
│  └─ app.db        # 런타임 자동 생성 (gitignore)
├─ static/         # index.html, app.js, style.css
├─ run.bat / run.py
└─ requirements.txt
```

## 데이터 추가·수정
- 지역·OTT·연예인·작품·장소는 모두 **app/catalog.py** 에서 편집한다.
- 편집 후 **data/app.db 를 삭제**하고 서버를 재시작하면 새 데이터로 다시 시드된다.
  (시드는 DB가 비어 있을 때만 동작한다.)

## 실행
```bash
# 1) 의존성
pip install -r requirements.txt

# 2) (질문 응답용) 로컬 모델 — 없어도 화면 흐름은 그대로 동작
#    https://ollama.com 설치 후:  ollama pull exaone3.5:2.4b

# 3) 실행 (셋 중 하나)
python run.py
#   또는  run.bat (Windows)
#   또는  uvicorn app.main:app --host 0.0.0.0 --port 8000

# 4) 브라우저: http://localhost:8000
```
- 다른 PC 접속: 같은 네트워크에서 `http://<서버 PC IP>:8000` (방화벽 8000 인바운드 허용이 필요할 수 있음)
- OpenAI 전환: 환경변수 `LLM_BASE_URL` / `LLM_MODEL` / `LLM_API_KEY` 설정

## API
| 메서드 | 경로 | 설명 |
|---|---|---|
| GET | /health | 상태 확인 |
| GET | /api/ui?lang | 화면 문구 |
| GET | /api/provinces?lang | 도 목록 |
| GET | /api/cities?province=&lang | 시·구 목록 |
| GET | /api/platforms?city=&lang | OTT 목록(동선 작품 수) |
| GET | /api/persons?city=&lang | 연예인 목록(동선 작품 수) |
| GET | /api/works?city=&platform=\|person=&lang | 작품 목록(인기순, 동선 유무) |
| GET | /api/route?city=&work=&lang | 작품 동선 |
| POST | /api/ask | 질문 응답 {city, work, question, lang} |

## 정확성 메모
촬영지·출연진·OTT 제공처는 공개자료(서울시 미디어허브 등) 기반이며 일부는 검증 중이다.
catalog.py 주석의 '검토' 표기 항목과 OTT 제공처·인기순서는 발표 전 1차 확인을 권장한다.
