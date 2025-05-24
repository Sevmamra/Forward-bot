from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from app.config import Config
from app.bot_data import bot_data
import logging

logger = logging.getLogger(__name__)

async def start_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Important to acknowledge the callback
    
    try:
        bot_data.reset()
        bot_data.collecting = True
        await query.edit_message_text(
            "📤 Send me videos, files, text messages etc.\n"
            "When finished, send /done command"
        )
    except Exception as e:
        logger.error(f"Error in start_process: {e}")
        await query.edit_message_text("❌ Error occurred. Please try again.")

def setup_callbacks(application):
    application.add_handler(
        CallbackQueryHandler(start_process, pattern="^start_process$")
    )
    # Add other callback handlers here as needed
