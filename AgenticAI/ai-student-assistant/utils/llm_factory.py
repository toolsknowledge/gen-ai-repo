"""
utils/llm_factory.py
────────────────────
Central factory for creating LLM instances.

WHY A FACTORY?
──────────────
Different agents need different models:
  • Supervisor / Answer Agent → claude-sonnet (smarter, slower, pricier)
  • Routing decisions → claude-haiku (faster, cheaper)

By centralising LLM creation here:
  • We avoid duplicating `ChatAnthropic(...)` boilerplate everywhere.
  • Switching to a different model or provider only needs a one-line change.
  • Tests can mock `create_llm()` to return a fake LLM.

CONCEPTS
────────
ChatAnthropic is a LangChain wrapper around the Anthropic SDK.
It exposes the same interface as ChatOpenAI so chains are provider-agnostic.

temperature=0  → deterministic output (great for routing & factual answers)
temperature=0.3 → slight creativity (good for synthesising narrative answers)
"""

from functools import lru_cache
from langchain_anthropic import ChatAnthropic
from config import settings
from utils.logger import get_logger

log = get_logger(__name__)


@lru_cache(maxsize=4)
def create_llm(
    model: str | None = None,
    temperature: float = 0.0,
    max_tokens: int = 2048,
) -> ChatAnthropic:
    """
    Return a cached ChatAnthropic instance.

    Parameters
    ──────────
    model        : Claude model string.  Defaults to settings.claude_smart_model.
    temperature  : 0 = deterministic, 1 = creative.
    max_tokens   : Maximum tokens in the LLM response.

    @lru_cache ensures we don't create a new HTTP client for every agent call.
    """
    chosen_model = model or settings.claude_smart_model

    log.debug("Creating LLM: model=%s  temp=%s", chosen_model, temperature)

    return ChatAnthropic(
        model=chosen_model,
        temperature=temperature,
        max_tokens=max_tokens,
        anthropic_api_key=settings.anthropic_api_key,
    )


def get_smart_llm() -> ChatAnthropic:
    """Sonnet – used by Answer Agent and Supervisor for complex reasoning."""
    return create_llm(model=settings.claude_smart_model, temperature=0.3)


def get_fast_llm() -> ChatAnthropic:
    """Haiku – used by Supervisor for quick routing decisions."""
    return create_llm(model=settings.claude_fast_model, temperature=0.0)
