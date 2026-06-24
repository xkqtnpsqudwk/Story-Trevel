"""F5 질문 응답 모듈 (로컬 모델 우선, 다국어).

역할: 질문에 '준비된 텍스트(근거)' 범위 안에서, 선택한 언어로 답한다.
기본 백엔드: 로컬 Ollama (OpenAI 호환 API, 요금 없음).
OpenAI 전환: LLM_BASE_URL / LLM_MODEL / LLM_API_KEY 환경변수 설정.
"""
import os

BASE_URL = os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1")
MODEL = os.environ.get("LLM_MODEL", "exaone3.5:2.4b")
API_KEY = os.environ.get("LLM_API_KEY", "ollama")

# 언어별 '범위 밖' 안내 + 시스템 프롬프트
OUT_OF_SCOPE = {
    "ko": "이번 동선에서 다루는 내용이 아니에요. 선택한 콘텐츠·장소에 대해 물어봐 주세요.",
    "en": "That's outside this route. Please ask about the selected show or places.",
}
SYS = {
    "ko": ("너는 서울 여행 안내봇이다. 아래 '근거 자료'에 있는 내용으로만 한국어로 답하라. "
           "근거에 없는 내용은 추측하지 말고, 정확히 다음 문장으로만 답하라: '{oos}'"),
    "en": ("You are a Seoul travel guide bot. Answer ONLY from the 'reference' below, in English. "
           "Do not guess beyond it; if it is not covered, reply exactly: '{oos}'"),
}


def _make_client():
    from openai import OpenAI
    if "localhost" in BASE_URL or "127.0.0.1" in BASE_URL:
        import httpx
        return OpenAI(base_url=BASE_URL, api_key=API_KEY,
                      http_client=httpx.Client(trust_env=False))
    return OpenAI(base_url=BASE_URL, api_key=API_KEY)


def answer_question(question: str, context_texts: list[str], lang: str = "ko") -> str:
    """질문에 대해 근거 텍스트 범위 내에서, 선택 언어로 답한다."""
    lang = lang if lang in SYS else "ko"
    system_prompt = SYS[lang].format(oos=OUT_OF_SCOPE[lang])
    ref_label = "근거 자료" if lang == "ko" else "Reference"
    q_label = "질문" if lang == "ko" else "Question"
    context = "\n".join(f"- {t}" for t in context_texts if t)
    try:
        client = _make_client()
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"[{ref_label}]\n{context}\n\n[{q_label}]\n{question}"},
            ],
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        if lang == "en":
            return ("Couldn't reach the AI. Make sure the local model (Ollama) is running.\n"
                    f"(config -> url: {BASE_URL}, model: {MODEL} / cause: {type(e).__name__})")
        return ("AI 응답을 불러오지 못했어요. 로컬 모델(Ollama)이 실행 중인지 확인해 주세요.\n"
                f"(현재 설정 → 주소: {BASE_URL}, 모델: {MODEL} / 원인: {type(e).__name__})\n"
                "준비: 1) ollama 설치 → 2) ollama pull " + MODEL + " → 3) ollama serve 실행")
