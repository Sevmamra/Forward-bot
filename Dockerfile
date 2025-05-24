FROM python:3.10-slim

# Set environment variables
ENV PYTHONPATH=/app

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

CMD ["python", "-m", "app.main"]
