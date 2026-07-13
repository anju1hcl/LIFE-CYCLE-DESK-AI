import os

try:
    import httpx
    from dotenv import load_dotenv
    from openai import OpenAI
except Exception:  # keeps app usable even before installing packages
    httpx = None
    OpenAI = None
    def load_dotenv():
        return None

load_dotenv()

_api_key = os.getenv("OPENAI_API_KEY")
_client = None

if _api_key and OpenAI is not None and httpx is not None:
    _client = OpenAI(
        api_key=_api_key,
        http_client=httpx.Client(verify=False),  # corporate SSL workaround for local demo
    )


def ask_llm(prompt: str, fallback: str = "") -> str:
    """Return an LLM response. If API/package is unavailable, return a deterministic fallback."""
    if not _client:
        return fallback or "LLM is not configured. Please install dependencies and set OPENAI_API_KEY."

    try:
        response = _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.25,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return fallback or f"LLM response unavailable: {exc}"
