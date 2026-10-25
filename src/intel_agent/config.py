import os
from dataclasses import dataclass

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (compatible; ai-signal/0.1; +https://github.com/zeeshah24/devin-projects)"
)


@dataclass(frozen=True)
class Settings:
    llm_api_key: str | None = None
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    fred_api_key: str | None = None
    http_timeout: float = 20.0
    enable_news_search: bool = False
    user_agent: str = DEFAULT_USER_AGENT

    @classmethod
    def from_env(cls) -> "Settings":
        timeout_raw = os.environ.get("HTTP_TIMEOUT")
        try:
            http_timeout = float(timeout_raw) if timeout_raw is not None else cls.http_timeout
        except ValueError:
            http_timeout = cls.http_timeout

        enable_news = os.environ.get("ENABLE_NEWS_SEARCH", "").strip().lower()

        return cls(
            llm_api_key=os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY") or None,
            llm_base_url=os.environ.get("LLM_BASE_URL", cls.llm_base_url).rstrip("/"),
            llm_model=os.environ.get("LLM_MODEL", cls.llm_model),
            fred_api_key=os.environ.get("FRED_API_KEY") or None,
            http_timeout=http_timeout,
            enable_news_search=enable_news in ("1", "true", "yes"),
            user_agent=os.environ.get("HTTP_USER_AGENT", DEFAULT_USER_AGENT),
        )
