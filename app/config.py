import os

class Config:
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  # Render se aayega
    AUTHORIZED_USER_ID = int(os.environ.get("AUTHORIZED_USER_ID", 0))
    GROUP_IDS = [int(x) for x in os.environ.get("GROUP_IDS", "").split(",") if x]
