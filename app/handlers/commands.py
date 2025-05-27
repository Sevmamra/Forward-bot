from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from app.config import Config
from app.bot_data import bot_data
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    if update.effective_user.id != Config.AUTHORIZED_USER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this bot!")
        return

    keyboard = [
        [InlineKeyboardButton("🚀 Start Forwarding", callback_data="start_process")]
    ]
    
    await update.message.reply_text(
        "🤖 Welcome to Forward Bot!\n\n"
        "1. Click 'Start Forwarding' to begin\n"
        "2. Send me files/videos/text to collect\n"
        "3. Use /done when finished",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /done command"""
    if update.effective_user.id != Config.AUTHORIZED_USER_ID:
        await update.message.reply_text("🚫 Not authorized!")
        return

    if not bot_data.collecting:
        await update.message.reply_text("⚠️ No active collection session!")
        return

    # Show collected items summary
    summary = (
        "📦 Collected Items:\n"
        f"🎥 Videos: {bot_data.received_items['videos']}\n"
        f"📷 Photos: {bot_data.received_items['photos']}\n"
        f"📄 Files: {bot_data.received_items['files']}\n"
        f"📝 Texts: {bot_data.received_items['texts']}\n"
        f"❔ Others: {bot_data.received_items['others']}"
    )

    keyboard = [
        [InlineKeyboardButton("📤 Select Groups", callback_data="select_groups")],
        [InlineKeyboardButton("❌ Cancel", callback_data="start_process")]
    ]

    await update.message.reply_text(
        summary,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "🆘 Bot Help Guide:\n\n"
        "1. /start - Begin forwarding process\n"
        "2. /done - Finish collecting items\n"
        "3. /help - Show this message\n\n"
        "⚠️ Note: Only authorized users can use this bot"
    )
    await update.message.reply_text(help_text)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command"""
    bot_data.reset()
    await update.message.reply_text("🛑 All operations cancelled!")

def setup_commands(application):
    """Register all command handlers"""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("done", done))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))
