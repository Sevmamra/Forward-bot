import os

class Config:
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID", 0))
    GROUP_IDS = [int(x) for x in os.getenv("GROUP_IDS", "").split(",") if x]
