# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Health check to verify bot can start
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "from app.config import Config; assert Config.TOKEN, 'Token not set!'" || exit 1

# Command to run the bot
CMD ["python", "-m", "app.main"]
