from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
from app.bot_data import bot_data

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_data.collecting:
        return

    # Save message for forwarding
    bot_data.messages_to_forward.append(update.message)

def setup_messages(application):
    handler = MessageHandler(
        filters.ChatType.PRIVATE & 
        (filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.TEXT),
        handle_message
    )
    application.add_handler(handler)
