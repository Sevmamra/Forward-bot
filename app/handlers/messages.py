from telegram.ext import MessageHandler, filters
from config import Config
from app.bot_data import bot_data

async def handle_message(update, context):
    if not bot_data.collecting or update.effective_user.id != Config.AUTHORIZED_USER_ID:
        return
    
    message = update.message
    if message.video:
        bot_data.received_items['videos'] += 1
    elif message.document:
        bot_data.received_items['files'] += 1
    else:
        bot_data.received_items['texts'] += 1

def setup_messages(application):
    application.add_handler(MessageHandler(
        filters.ChatType.PRIVATE & ~filters.COMMAND,
        handle_message
    ))
