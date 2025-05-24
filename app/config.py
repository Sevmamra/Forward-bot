import os

class Config:
    TOKEN = os.getenv("7763888885:AAGGtCSMRc0tvvGCFJwRMmYJBR819JfiOmQ")
    AUTHORIZED_USER_ID = int(os.getenv("6567162029", 0))
    GROUP_IDS = [int(x) for x in os.getenv("-1002501498159", "-1002665578655").split(",") if x]
