from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from app.config import Config
from app.bot_data import bot_data
import logging

logger = logging.getLogger(__name__)

# ... [keep previous callback functions until select_groups] ...

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
    
    # Add SELECT TOPICS button for selected groups
    if bot_data.selected_groups:
        keyboard.append([
            InlineKeyboardButton("📌 SELECT TOPICS", callback_data="select_topics")
        ])
    
    keyboard.append([
        InlineKeyboardButton("🔘 Select All Groups", callback_data="select_all_groups"),
        InlineKeyboardButton("🚀 Send", callback_data="proceed_to_forward")
    ])
    
    await query.edit_message_text(
        "👇 Select Groups & Topics:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def select_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for group_id in bot_data.selected_groups:
        await bot_data.fetch_topics(context, group_id)
        group_name = bot_data.groups_info[group_id]['name']
        
        # Add group header
        keyboard.append([InlineKeyboardButton(f"--- {group_name} ---", callback_data="none")])
        
        # Add topics
        for topic_id, topic_name in bot_data.groups_info[group_id]['topics'].items():
            selected = "✅" if topic_id in bot_data.selected_groups.get(group_id, set()) else "◻️"
            keyboard.append([
                InlineKeyboardButton(
                    f"{topic_name} {selected}",
                    callback_data=f"toggle_topic:{group_id}:{topic_id}"
                )
            ])
    
    # Add CREATE NEW TOPIC button
    keyboard.append([
        InlineKeyboardButton("✨ CREATE NEW TOPIC", callback_data="create_new_topic")
    ])
    
    # Add back button
    keyboard.append([
        InlineKeyboardButton("🔙 Back to Groups", callback_data="select_groups")
    ])
    
    await query.edit_message_text(
        "📌 Select Topics for Forwarding:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def toggle_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, group_id, topic_id = query.data.split(":")
    group_id = int(group_id)
    topic_id = int(topic_id)
    
    if group_id not in bot_data.selected_groups:
        bot_data.selected_groups[group_id] = set()
    
    if topic_id in bot_data.selected_groups[group_id]:
        bot_data.selected_groups[group_id].remove(topic_id)
    else:
        bot_data.selected_groups[group_id].add(topic_id)
    
    await select_topics(update, context)

async def create_new_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📝 Send the name for new topic:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="select_topics")]
        ])
    )
    return "WAITING_FOR_TOPIC_NAME"

async def handle_new_topic_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic_name = update.message.text
    # Implement topic creation logic here
    await update.message.reply_text(
        f"✅ Topic '{topic_name}' created!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Continue", callback_data="select_topics")]
        ])
    )
    return -1  # End conversation

def setup_callbacks(application):
    # ... [previous handlers] ...
    application.add_handler(CallbackQueryHandler(select_topics, pattern="^select_topics$"))
    application.add_handler(CallbackQueryHandler(toggle_topic, pattern="^toggle_topic:"))
    application.add_handler(CallbackQueryHandler(create_new_topic, pattern="^create_new_topic$"))
    
    # Add conversation handler for topic creation
    from telegram.ext import ConversationHandler
    application.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(create_new_topic, pattern="^create_new_topic$")],
        states={
            "WAITING_FOR_TOPIC_NAME": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_topic_name)]
        },
        fallbacks=[]
    ))
