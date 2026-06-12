import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")

# Bot Settings
BOT_NAME = "Jarvis AI Assistant"
BOT_VERSION = "2.0.0"
DEFAULT_LANGUAGE = "tr"
MAX_HISTORY_LENGTH = 20

# Modes
MODE_ONLINE = "online"
MODE_OFFLINE = "offline"
DEFAULT_MODE = MODE_ONLINE

# Jarvis Mode
JARVIS_GREETING = "Efendim, size nasıl yardımcı olabilirim?"
JARVIS_PREFIX = "Efendim"
