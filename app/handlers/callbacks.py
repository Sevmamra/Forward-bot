from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from app.config import Config
from app.bot_data import bot_data
async def start_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the forwarding process."""
    query = update.callback_query
    await query.answer()
    
    bot_data.reset()
    bot_data.collecting = True
    await query.edit_message_text(
        "📤 Send me videos, files, text messages etc.\n"
        "When finished, send /done command\n\n"
        "I'll count all received items automatically!"
    )

# Other callback handlers...

def setup_callbacks(application):
    """Register callback query handlers."""
    application.add_handler(CallbackQueryHandler(start_process, pattern="^start_process$"))
    # Add other callback handlers...
