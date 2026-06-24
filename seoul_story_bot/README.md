# 서울 스토리 동선 추천 AI봇 (MVP)

좋아하는 K-콘텐츠를 고르면, 서울 속 배경 장소(실제 촬영지·세계관 원형)를
하나의 동선으로 묶어 이야기와 주변 체험을 안내하는 데모.

## 기술 스택
- 백엔드: FastAPI (Python)
- 프론트엔드: 정적 HTML + 바닐라 JS
- 데이터: JSON 파일 (`data/contents.json`)
- AI(질문 응답, F5): 로컬 모델 Ollama 기본(요금 없음). OpenAI API로도 전환 가능

## 폴더 구조
```
seoul_story_bot/
├─ app/
│  ├─ main.py        # FastAPI 서버 (라우트)
│  └─ llm.py         # F5 질문 응답 (근거 주입)
├─ data/contents.json # 콘텐츠·장소·동선·매핑
├─ static/           # index.html, app.js, style.css
└─ requirements.txt
```

## 실행 방법
```bash
# 1) 의존성 설치
pip install -r requirements.txt

# 2) (질문 응답 F5용) 로컬 모델 준비 — 요금 없음
#    - https://ollama.com 에서 Ollama 설치 (설치하면 localhost:11434에 자동 실행)
#    - 한국어 모델 받기:  ollama pull exaone3.5   (대안: qwen2.5, gemma2)
#    설치 안 해도 F1~F4 화면 흐름은 그대로 동작합니다.

# 3) 서버 실행
uvicorn app.main:app --reload

# 4) 브라우저에서 열기:  http://127.0.0.1:8000

# (선택) OpenAI로 바꾸려면 환경변수만 설정
#   Windows:  set LLM_BASE_URL=https://api.openai.com/v1 & set LLM_MODEL=gpt-4o-mini & set LLM_API_KEY=sk-...
```

## 기능 (MVP)
- F1 콘텐츠 선택  → F2 동선 추천  → F3 장소별 스토리 해설
- F4 주변 테마 체험 안내  → F5 질문 응답(준비된 텍스트 범위 내)

## 확정 데모 동선
- 폭군의 셰프: 운경고택(실제 촬영지) → 경복궁 소주방(세계관 원형)
- 참교육: 서울 중앙고등학교(실제 촬영지) → CU 삼청점(실제 촬영지)
- 모두 종로 도보권.

## 주의 (다음 작업)
- 해설(story_text/place_story)은 **초안**이며 1차 자료로 고증 검수가 필요합니다.
- 촬영지 정보는 전문 블로그 기반이라 공식 1차 확인이 권장됩니다.
- 방문 조건(운경고택 개방, 중앙고 현역 학교, 소주방 시식 행사 일정 등)은 별도 확인.

## 다른 PC에서 접속하기

지금 기본 실행은 내 PC에서만 보입니다. 다른 PC가 접속하려면 서버를
`0.0.0.0`(모든 네트워크에서 수신)으로 열어야 합니다.

### 실행 (둘 중 하나)
```bash
python run.py
# 또는
uvicorn app.main:app --host 0.0.0.0 --port 8000
# (Windows는 run.bat 더블클릭도 가능)
```

### A. 같은 네트워크(같은 공유기/와이파이)의 다른 PC
1. 위 명령으로 서버 실행
2. 내 PC의 IP 확인
   - Windows: 명령 프롬프트에서 `ipconfig` → "IPv4 주소" (예: 192.168.0.10)
   - macOS/Linux: `ifconfig` 또는 `ip addr`
3. 다른 PC 브라우저에서 접속: `http://192.168.0.10:8000`
4. 안 되면 **방화벽에서 8000 포트(또는 Python)를 허용**
   - Windows: "Windows Defender 방화벽 > 앱 허용"에서 Python 허용

### B. 인터넷 어디서나(외부 네트워크의 PC)
같은 공유기가 아니면, 임시 공개 주소(터널)를 쓰는 게 가장 쉽습니다.
```bash
# 예) ngrok (https://ngrok.com 설치 후)
ngrok http 8000
# 발급된 https 주소(예: https://xxxx.ngrok-free.app)를 상대에게 공유
```
또는 Cloudflare Tunnel(`cloudflared tunnel --url http://localhost:8000`)도 가능합니다.

### 주의
- `0.0.0.0`으로 열면 네트워크의 다른 기기가 접속할 수 있으니, 신뢰된 망에서만 쓰세요.
- 터널(ngrok 등)은 **임시 공개**입니다. 데모가 끝나면 종료하세요.
- OpenAI 키는 서버(내 PC)에만 두므로 접속자에게 노출되지 않습니다.
- 영구적으로 공개하려면 클라우드 배포(Render·Railway 등)가 필요하며, 이는 추후 과제입니다.
