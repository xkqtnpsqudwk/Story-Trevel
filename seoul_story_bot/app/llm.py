"""F5 질문 응답 모듈 (로컬 모델 우선).

역할: 사용자의 질문에 '준비된 텍스트(근거)' 범위 안에서만 답한다.
왜 필요한가: 설계서 F5 원칙(콘텐츠 범위 한정)으로 고증 오류·환각을 막기 위해서.
흐름: 질문 + 근거 텍스트 → LLM에 전달 → 근거 안에서만 답변(없으면 '범위 밖' 안내).

기본 백엔드: 로컬 Ollama (OpenAI 호환 API, 요금 없음).
  - Ollama는 http://localhost:11434/v1 에 OpenAI 호환 엔드포인트를 제공하므로
    OpenAI 파이썬 SDK를 그대로 쓰되 base_url만 로컬로 바꾼다.
OpenAI로 바꾸려면 환경변수만 바꾸면 된다:
  LLM_BASE_URL=https://api.openai.com/v1  LLM_MODEL=gpt-4o-mini  LLM_API_KEY=sk-...
"""
import os

BASE_URL = os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1")
MODEL = os.environ.get("LLM_MODEL", "exaone3.5")   # 한국어 강한 로컬 모델 예시
API_KEY = os.environ.get("LLM_API_KEY", "ollama")   # Ollama는 키 불필요(더미값)

OUT_OF_SCOPE_MSG = "이번 동선에서 다루는 내용이 아니에요. 선택한 콘텐츠·장소에 대해 물어봐 주세요."

SYSTEM_PROMPT = (
    "너는 서울 여행 안내봇이다. 아래 '근거 자료'에 있는 내용으로만 한국어로 답하라. "
    "근거에 없는 내용은 추측하지 말고, 정확히 다음 문장으로만 답하라: "
    f"'{OUT_OF_SCOPE_MSG}'"
)


def _make_client():
    """LLM 클라이언트 생성. 로컬 주소는 프록시를 타지 않게 한다."""
    from openai import OpenAI
    if "localhost" in BASE_URL or "127.0.0.1" in BASE_URL:
        # 학교·회사 프록시 환경에서 로컬 호출이 막히는 문제 예방
        import httpx
        return OpenAI(base_url=BASE_URL, api_key=API_KEY,
                      http_client=httpx.Client(trust_env=False))
    return OpenAI(base_url=BASE_URL, api_key=API_KEY)


def answer_question(question: str, context_texts: list[str]) -> str:
    """질문에 대해 근거 텍스트 범위 내에서 답한다."""
    context = "\n".join(f"- {t}" for t in context_texts if t)
    try:
        client = _make_client()
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"[근거 자료]\n{context}\n\n[질문]\n{question}"},
            ],
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return (
            "AI 응답을 불러오지 못했어요. 로컬 모델(Ollama)이 실행 중인지 확인해 주세요.\n"
            f"(현재 설정 → 주소: {BASE_URL}, 모델: {MODEL} / 원인: {type(e).__name__})\n"
            "준비: 1) ollama 설치 → 2) ollama pull " + MODEL + " → 3) ollama serve 실행"
        )
