from . import config


class TG:
    def __init__(self, client):
        self.client = client
        self.base = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}"

    async def call(self, method, timeout=30, **kw):
        r = await self.client.post(f"{self.base}/{method}", timeout=timeout, **kw)
        data = r.json()
        if not data.get("ok"):
            raise RuntimeError(f"Telegram {method} failed: {data.get('description')}")
        return data["result"]

    async def updates(self, offset):
        return await self.call("getUpdates", timeout=45, json={"offset": offset, "timeout": 30, "allowed_updates": ["message"]})

    async def send(self, chat_id, text):
        return await self.call("sendMessage", json={"chat_id": chat_id, "text": text})

    async def send_audio(self, chat_id, wav: bytes):
        return await self.call("sendAudio", data={"chat_id": chat_id}, files={"audio": ("reply.wav", wav, "audio/wav")})

    async def send_document(self, chat_id, name, content: bytes):
        return await self.call("sendDocument", data={"chat_id": chat_id}, files={"document": (name, content)})

    async def download(self, file_id) -> bytes:
        f = await self.call("getFile", json={"file_id": file_id})
        r = await self.client.get(f"https://api.telegram.org/file/bot{config.TELEGRAM_TOKEN}/{f['file_path']}", timeout=60)
        r.raise_for_status()
        return r.content
