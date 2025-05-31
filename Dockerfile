FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import os; assert os.getenv('TELEGRAM_BOT_TOKEN'), 'Token not set!'" || exit 1

# Run bot
CMD ["python", "-m", "app.main"]
