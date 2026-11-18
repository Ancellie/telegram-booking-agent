import asyncio
import json

from . import config

BASE = "https://api.groq.com/openai/v1"


def _h():
    return {"Authorization": f"Bearer {config.GROQ_API_KEY}"}


async def chat_json(client, messages):
    """Returns (parsed_json_or_None, error_text)."""
    body = {"model": config.LLM_MODEL, "messages": messages, "temperature": 0.3,
            "max_completion_tokens": 1500, "response_format": {"type": "json_object"}}
    if "gpt-oss" in config.LLM_MODEL:
        body["reasoning_effort"] = "low"
    err = ""
    for _ in range(3):
        try:
            r = await client.post(f"{BASE}/chat/completions", headers=_h(), json=body, timeout=60)
            r.raise_for_status()
            c = r.json()["choices"][0]["message"]["content"] or ""
            return json.loads(c[c.index("{"): c.rindex("}") + 1]), ""
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__}: {e}"
            await asyncio.sleep(2)
    return None, err


async def stt(client, audio: bytes) -> str:
    r = await client.post(f"{BASE}/audio/transcriptions", headers=_h(),
                          files={"file": ("voice.ogg", audio, "audio/ogg")},
                          data={"model": config.STT_MODEL, "response_format": "json"}, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"STT {r.status_code}: {r.text[:300]}")
    return (r.json().get("text") or "").strip()


async def tts(client, text: str) -> bytes:
    r = await client.post(f"{BASE}/audio/speech", headers=_h(), timeout=60,
                          json={"model": config.TTS_MODEL, "voice": config.TTS_VOICE, "input": text, "response_format": "wav"})
    if r.status_code >= 400:
        raise RuntimeError(f"TTS {r.status_code}: {r.text[:300]}")
    return r.content
