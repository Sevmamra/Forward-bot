# Telegram Forward Bot

A simple bot to forward messages to multiple groups/topics.

## Features
- Forward messages, videos, files to multiple groups
- Support for topics in groups
- Admin-only access

## Setup
1. Clone this repository
2. Set environment variables:
   - `TELEGRAM_BOT_TOKEN` - Your bot token
   - `AUTHORIZED_USER_ID` - Your Telegram user ID
   - `GROUP_IDS` - Comma-separated group IDs (-100123,...)

## Deployment
```bash
docker build -t telegram-bot .
docker run -e TELEGRAM_BOT_TOKEN="xxx" -e AUTHORIZED_USER_ID=123 telegram-bot
