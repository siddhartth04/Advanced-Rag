import json
import litellm
from rag.config import settings


async def call_llm(messages: list[dict], json_mode: bool = False) -> str:
    kwargs: dict = dict(
        model=settings.llm_model,
        messages=messages,
    )
    if settings.llm_api_base:
        kwargs["api_base"] = settings.llm_api_base
    if settings.llm_api_key:
        kwargs["api_key"] = settings.llm_api_key
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = await litellm.acompletion(**kwargs)
    return response.choices[0].message.content


async def call_llm_json(messages: list[dict]) -> dict:
    raw = await call_llm(messages, json_mode=True)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        cleaned = raw.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(cleaned)


async def stream_llm(messages: list[dict]):
    """Yields string chunks for SSE streaming."""
    kwargs: dict = dict(
        model=settings.llm_model,
        messages=messages,
        stream=True,
    )
    if settings.llm_api_base:
        kwargs["api_base"] = settings.llm_api_base
    if settings.llm_api_key:
        kwargs["api_key"] = settings.llm_api_key
    async for chunk in await litellm.acompletion(**kwargs):
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
