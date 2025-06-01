from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from app.bot_data import bot_data

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("🚀 Start Forwarding", callback_data="start_process")
    ]]
    await update.message.reply_text(
        "📤 Send me files/videos/text. When done, use /done",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_data.collecting:
        await update.message.reply_text("⚠️ No active collection!")
        return

    keyboard = [[
        InlineKeyboardButton("📝 Create New Topic", callback_data="create_topic")
    ]]
    await update.message.reply_text(
        f"📊 Collected: {len(bot_data.messages_to_forward)} items\n"
        "Click below to create new topic:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def setup_commands(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("done", done))
