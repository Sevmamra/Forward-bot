from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from app.config import Config
from app.bot_data import bot_data
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized!")
        return

    keyboard = [[
        InlineKeyboardButton("🚀 Start Forwarding", callback_data="start_process")
    ]]
    await update.message.reply_text(
        "📤 Send me files/videos/text. When done, use /done",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_data.collecting:
        await update.message.reply_text("⚠️ No active session!")
        return

    keyboard = [[
        InlineKeyboardButton("📝 Create New Topic", callback_data="create_topic")
    ]]
    await update.message.reply_text(
        f"📊 Collected: {len(bot_data.messages_to_forward)} items\n"
        "Click below to create new topic and forward:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def setup_commands(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("done", done))
