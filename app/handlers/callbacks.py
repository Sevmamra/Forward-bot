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
from app.utils.telegram_utils import fetch_topics, create_topic

logger = logging.getLogger(__name__)

WAITING_FOR_TOPIC_NAME = 1

async def cancel_topic_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Topic creation cancelled.")
    return ConversationHandler.END

async def start_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    bot_data.reset()
    bot_data.collecting = True
    await query.edit_message_text("📤 Send me videos, files, text messages etc.\nWhen finished, send /done command")

async def select_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not bot_data.groups_info:
        await bot_data.fetch_groups(context)

    keyboard = []
    for group_id, group_info in bot_data.groups_info.items():
        selected = "✅" if group_id in bot_data.selected_groups else "◻️"
        keyboard.append([
            InlineKeyboardButton(
                f"{group_info['name']} {selected}",
                callback_data=f"toggle_group:{group_id}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("🔘 Select All", callback_data="select_all_groups"),
        InlineKeyboardButton("🚀 Send Now", callback_data="proceed_to_forward")
    ])

    await query.edit_message_text(
        "🔍 Select Groups to Forward:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def toggle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    group_id = int(query.data.split(":")[1])

    if group_id in bot_data.selected_groups:
        bot_data.selected_groups.pop(group_id, None)
    else:
        bot_data.selected_groups[group_id] = set()

    await select_groups(update, context)

async def select_all_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    bot_data.selected_groups = {group_id: set() for group_id in bot_data.groups_info}
    await select_groups(update, context)

async def select_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []
    for group_id in bot_data.selected_groups:
        bot_data.groups_info[group_id]['topics'] = await fetch_topics(context.bot, group_id)
        group_name = bot_data.groups_info[group_id]['name']

        keyboard.append([InlineKeyboardButton(f"🏷️ {group_name}", callback_data="none")])
        
        for topic_id, topic_name in bot_data.groups_info[group_id]['topics'].items():
            selected = "✅" if topic_id in bot_data.selected_groups[group_id] else "◻️"
            keyboard.append([
                InlineKeyboardButton(
                    f"{topic_name} {selected}",
                    callback_data=f"toggle_topic:{group_id}:{topic_id}"
                )
            ])

    keyboard.append([
        InlineKeyboardButton("✨ New Topic", callback_data="create_new_topic"),
        InlineKeyboardButton("🔙 Back", callback_data="select_groups")
    ])

    await query.edit_message_text(
        "📌 Select Topics for Each Group:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def toggle_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, group_id, topic_id = query.data.split(":")
    group_id = int(group_id)
    topic_id = int(topic_id)

    if topic_id in bot_data.selected_groups[group_id]:
        bot_data.selected_groups[group_id].remove(topic_id)
    else:
        bot_data.selected_groups[group_id].add(topic_id)

    await select_topics(update, context)

async def create_new_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📝 Enter new topic name:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="select_topics")]
        ])
    )
    return WAITING_FOR_TOPIC_NAME

async def handle_new_topic_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic_name = update.message.text
    group_id = next(iter(bot_data.selected_groups))
    
    topic_id = await create_topic(context.bot, group_id, topic_name)
    if topic_id:
        bot_data.groups_info[group_id]['topics'][topic_id] = topic_name
        bot_data.selected_groups[group_id].add(topic_id)
        await update.message.reply_text(f"✅ Topic '{topic_name}' created!")
    else:
        await update.message.reply_text("❌ Failed to create topic!")
    
    return ConversationHandler.END

async def proceed_to_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    total_sent = 0
    for msg_data in bot_data.messages_to_forward:
        for group_id, topic_ids in bot_data.selected_groups.items():
            for topic_id in topic_ids:
                try:
                    kwargs = {
                        'chat_id': group_id,
                        'message_thread_id': topic_id
                    }
                    if msg_data['type'] == 'video':
                        await context.bot.send_video(video=msg_data['content'], **kwargs)
                    elif msg_data['type'] == 'photo':
                        await context.bot.send_photo(photo=msg_data['content'], **kwargs)
                    elif msg_data['type'] == 'document':
                        await context.bot.send_document(document=msg_data['content'], **kwargs)
                    elif msg_data['type'] == 'text':
                        await context.bot.send_message(text=msg_data['content'], **kwargs)
                    total_sent += 1
                except Exception as e:
                    logger.error(f"Forward error: {e}")

    await query.edit_message_text(f"✅ Forwarded {total_sent} items")
    bot_data.reset()

def setup_callbacks(application):
    application.add_handler(CallbackQueryHandler(start_process, pattern="^start_process$"))
    application.add_handler(CallbackQueryHandler(select_groups, pattern="^select_groups$"))
    application.add_handler(CallbackQueryHandler(toggle_group, pattern="^toggle_group:"))
    application.add_handler(CallbackQueryHandler(select_all_groups, pattern="^select_all_groups$"))
    application.add_handler(CallbackQueryHandler(select_topics, pattern="^select_topics$"))
    application.add_handler(CallbackQueryHandler(toggle_topic, pattern="^toggle_topic:"))
    application.add_handler(CallbackQueryHandler(proceed_to_forward, pattern="^proceed_to_forward$"))

    application.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(create_new_topic, pattern="^create_new_topic$")],
        states={
            WAITING_FOR_TOPIC_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_topic_name),
                MessageHandler(filters.COMMAND | filters.Regex("^❌ Cancel$"), cancel_topic_creation)
            ]
        },
        fallbacks=[]
    ))
