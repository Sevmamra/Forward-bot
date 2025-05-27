FROM python:3.10-slim

WORKDIR /app

# पहले Python-Telegram-Bot के डिपेंडेंसीज इंस्टॉल करो
COPY requirements.txt .
RUN pip install --no-cache-dir python-telegram-bot==20.5 python-dotenv==1.0.0 httpx==0.24.1

# फिर FastAPI/UVicorn अलग से इंस्टॉल करो
RUN pip install --no-cache-dir fastapi==0.109.2 uvicorn==0.27.1

COPY . .

CMD ["python", "-m", "app.main"]
