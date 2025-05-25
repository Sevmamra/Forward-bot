from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from app.bot_data import bot_data
from app.config import Config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return

    keyboard = [
        [InlineKeyboardButton("🚀 Start Process", callback_data="start_process")]
    ]

    await update.message.reply_text(
        "👋 Welcome! Use the button below to start forwarding process.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_data.collecting:
        await update.message.reply_text("⚠️ No active collection in progress.")
        return

    summary = (
        "✅ Collection Summary:\n"
        f"📹 Videos: {bot_data.received_items['videos']}\n"
        f"📄 Files: {bot_data.received_items['files']}\n"
        f"🖼️ Photos: {bot_data.received_items['photos']}\n"
        f"📝 Texts: {bot_data.received_items['texts']}\n"
        f"📦 Others: {bot_data.received_items['others']}\n\n"
        "Select what to do next:"
    )

    keyboard = [
        [InlineKeyboardButton("📤 SELECT GROUPS", callback_data="select_groups")],
        [InlineKeyboardButton("❌ Cancel", callback_data="start_process")]
    ]

    await update.message.reply_text(
        summary,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def setup_commands(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("done", done))
