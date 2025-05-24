import os
from typing import List, Union

class Config:
    # Telegram API credentials
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    API_ID = int(os.getenv("TELEGRAM_API_ID", 0))
    API_HASH = os.getenv("TELEGRAM_API_HASH")
    
    # Bot configuration
    AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID", 0))
    GROUP_IDS = [int(x) for x in os.getenv("GROUP_IDS", "").split(",") if x]
    
    # Redis configuration (for production)
    REDIS_URL = os.getenv("REDIS_URL")
    
    # Webhook settings
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    WEBHOOK_PATH = f"/webhook/{TOKEN}"
    PORT = int(os.getenv("PORT", 8000))
