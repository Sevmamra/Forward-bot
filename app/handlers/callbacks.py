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

# --------------------------
# HELPER FUNCTIONS
# --------------------------
async def cancel_topic_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Topic creation cancelled.")
    return ConversationHandler.END

async def _check_forum_group(bot, group_id):
    """Check if group has topics enabled"""
    try:
        chat = await bot.get_chat(group_id)
        return chat.is_forum
    except Exception as e:
        logger.error(f"Forum check failed: {e}")
        return False

# --------------------------
# MAIN HANDLERS
# --------------------------
async def start_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    bot_data.reset()
    bot_data.collecting = True
    await query.edit_message_text(
        "📤 Send me videos/files/text to forward.\n"
        "Send /done when finished."
    )

async def select_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not bot_data.groups_info:
        await bot_data.fetch_groups(context)

    keyboard = []
    valid_groups = 0
    
    for group_id, group_info in bot_data.groups_info.items():
        is_forum = await _check_forum_group(context.bot, group_id)
        if not is_forum:
            keyboard.append([
                InlineKeyboardButton(
                    f"❌ {group_info['name']} (Enable Topics)",
                    callback_data="invalid_group"
                )
            ])
            continue

        valid_groups += 1
        selected = "✅" if group_id in bot_data.selected_groups else "◻️"
        keyboard.append([
            InlineKeyboardButton(
                f"{group_info['name']} {selected}",
                callback_data=f"toggle_group:{group_id}"
            )
        ])

    # Only show topics button if valid forum groups selected
    if valid_groups > 0:
        keyboard.append([
            InlineKeyboardButton("📌 SELECT TOPICS", callback_data="select_topics")
        ])

    keyboard.extend([
        [InlineKeyboardButton("🔘 Select All", callback_data="select_all_groups")],
        [InlineKeyboardButton("🚀 Send Now", callback_data="proceed_to_forward")]
    ])

    await query.edit_message_text(
        "🔍 Select Groups (Only groups with Topics enabled will work):",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def toggle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    group_id = int(query.data.split(":")[1])

    if group_id in bot_data.selected_groups:
        bot_data.selected_groups.pop(group_id, None)
    else:
        bot_data.selected_groups[group_id] = set()  # Initialize empty topics set

    await select_groups(update, context)

async def select_all_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    bot_data.selected_groups = {}
    for group_id in bot_data.groups_info:
        if await _check_forum_group(context.bot, group_id):
            bot_data.selected_groups[group_id] = set()

    await select_groups(update, context)

async def select_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []
    for group_id in bot_data.selected_groups:
        if not await _check_forum_group(context.bot, group_id):
            continue

        topics = await fetch_topics(context.bot, group_id)
        if not topics:
            keyboard.append([
                InlineKeyboardButton(
                    f"❌ No topics in {bot_data.groups_info[group_id]['name']}",
                    callback_data="none"
                )
            ])
            continue

        keyboard.append([
            InlineKeyboardButton(
                f"📌 {bot_data.groups_info[group_id]['name']}",
                callback_data="none"
            )
        ])

        for topic_id, topic_name in topics.items():
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
        "📌 Select Topics:",
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
    
    if not bot_data.selected_groups:
        await query.edit_message_text("❌ No groups selected!")
        return

    await query.edit_message_text(
        "📝 Send new topic name:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="select_topics")]
        ])
    )
    return WAITING_FOR_TOPIC_NAME

async def handle_new_topic_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic_name = update.message.text
    if not topic_name.strip():
        await update.message.reply_text("❌ Topic name cannot be empty!")
        return WAITING_FOR_TOPIC_NAME

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

    if not any(bot_data.selected_groups.values()):
        await query.edit_message_text("❌ No topics selected!")
        return

    total_sent = 0
    for msg_data in bot_data.messages_to_forward:
        for group_id, topic_ids in bot_data.selected_groups.items():
            for topic_id in topic_ids:
                try:
                    kwargs = {
                        'chat_id': group_id,
                        'message_thread_id': topic_id,
                        'caption': msg_data.get('caption')
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
                    logger.error(f"Forward failed: {e}")

    await query.edit_message_text(f"🚀 Forwarded {total_sent} items successfully!")
    bot_data.reset()

# --------------------------
# SETUP FUNCTION
# --------------------------
def setup_callbacks(application):
    # Button handlers
    application.add_handler(CallbackQueryHandler(start_process, pattern="^start_process$"))
    application.add_handler(CallbackQueryHandler(select_groups, pattern="^select_groups$"))
    application.add_handler(CallbackQueryHandler(toggle_group, pattern="^toggle_group:"))
    application.add_handler(CallbackQueryHandler(select_all_groups, pattern="^select_all_groups$"))
    application.add_handler(CallbackQueryHandler(select_topics, pattern="^select_topics$"))
    application.add_handler(CallbackQueryHandler(toggle_topic, pattern="^toggle_topic:"))
    application.add_handler(CallbackQueryHandler(proceed_to_forward, pattern="^proceed_to_forward$"))
    application.add_handler(CallbackQueryHandler(select_groups, pattern="^invalid_group$"))

    # Conversation handler for topic creation
    application.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(create_new_topic, pattern="^create_new_topic$")],
        states={
            WAITING_FOR_TOPIC_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_topic_name),
                MessageHandler(filters.COMMAND | filters.Regex("^❌ Cancel$"), cancel_topic_creation)
            ]
        },
        fallbacks=[],
        per_message=False
    ))
