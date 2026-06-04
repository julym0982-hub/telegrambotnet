
import os

class Config:
    # Admin Bot (aiogram) settings
    BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID", 123456789))  # Replace with your Telegram Admin User ID

    # Userbot (Pyrogram) settings
    API_ID = int(os.getenv("API_ID", 123456))  # Get from my.telegram.org
    API_HASH = os.getenv("API_HASH", "YOUR_API_HASH") # Get from my.telegram.org
    # SESSION_STRING is for multiple userbot accounts. Each string represents a userbot session.
    # You can generate session strings using a separate Pyrogram script.
    SESSION_STRINGS = os.getenv("SESSION_STRINGS", "").split(",") # Comma separated session strings

    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/bot.db")

    # APScheduler settings
    DEFAULT_SEND_INTERVAL_MINUTES = int(os.getenv("DEFAULT_SEND_INTERVAL_MINUTES", 5))

    # Anti-Ban & Anti-Spam settings
    MIN_RANDOM_DELAY = int(os.getenv("MIN_RANDOM_DELAY", 10)) # seconds
    MAX_RANDOM_DELAY = int(os.getenv("MAX_RANDOM_DELAY", 30)) # seconds

    # Spintax example: {Hello|Hi} there! I'm {a bot|an automated system}.
    # This will be used if the message stored in DB does not contain spintax.
    DEFAULT_SPINTAX_MESSAGE = os.getenv("DEFAULT_SPINTAX_MESSAGE", "{Hello|Hi} from your userbot!")
