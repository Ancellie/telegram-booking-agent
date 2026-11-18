import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MANAGER_USERNAME = os.getenv("MANAGER_USERNAME", "defaultusername").strip().lstrip("@").lower()
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "").strip().lstrip("@").lower()  # optional: only this user is the client
TZ = os.getenv("RESTAURANT_TZ", "Europe/London")
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")
STT_MODEL = os.getenv("STT_MODEL", "whisper-large-v3-turbo")
TTS_MODEL = os.getenv("TTS_MODEL", "canopylabs/orpheus-v1-english")
TTS_VOICE = os.getenv("TTS_VOICE", "hannah")
VOICE_REPLIES = os.getenv("VOICE_REPLIES", "on").lower() in ("on", "yes", "true", "1")
DB_PATH = os.getenv("DB_PATH", "data/agent.db")
