from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler
)
from app.config import Config
from app.bot_data import bot_data
import logging

logger = logging.getLogger(__name__)

WAITING_FOR_TOPIC_NAME = 1

async def start_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data.reset()
    bot_data.collecting = True
    await update.callback_query.edit_message_text("📥 Ready to collect messages!")

async def create_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "📝 Send name for new topic:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_process")
        ]])
    )
    return WAITING_FOR_TOPIC_NAME

async def handle_topic_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic_name = update.message.text
    if not topic_name.strip():
        await update.message.reply_text("❌ Invalid name!")
        return WAITING_FOR_TOPIC_NAME

    # Create topic in first available group
    group_id = Config.GROUP_IDS[0]
    try:
        topic = await context.bot.create_forum_topic(
            chat_id=group_id,
            name=topic_name
        )
        
        # Forward all collected messages
        success = 0
        for msg in bot_data.messages_to_forward:
            try:
                await msg.forward(
                    chat_id=group_id,
                    message_thread_id=topic.message_thread_id
                )
                success += 1
            except Exception as e:
                logger.error(f"Forward failed: {e}")

        await update.message.reply_text(
            f"✅ Forwarded {success}/{len(bot_data.messages_to_forward)} items "
            f"to topic: {topic_name}"
        )
    except Exception as e:
        logger.error(f"Topic creation failed: {e}")
        await update.message.reply_text("❌ Failed to create topic!")

    bot_data.reset()
    return ConversationHandler.END

async def cancel_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data.reset()
    await update.callback_query.edit_message_text("❌ Operation cancelled!")

def setup_callbacks(application):
    application.add_handler(CallbackQueryHandler(
        start_process, pattern="^start_process$"
    ))
    application.add_handler(CallbackQueryHandler(
        cancel_process, pattern="^cancel_process$"
    ))
    
    application.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(
            create_topic, pattern="^create_topic$"
        )],
        states={
            WAITING_FOR_TOPIC_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    handle_topic_name
                )
            ]
        },
        fallbacks=[]
    ))
