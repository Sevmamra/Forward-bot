from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from app.config import Config
from app.bot_data import bot_data
import logging

logger = logging.getLogger(__name__)

async def select_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Fetch groups if not already loaded
    if not bot_data.groups_info:
        await bot_data.fetch_groups(context)
    
    if not bot_data.groups_info:
        await query.edit_message_text("❌ No groups found where I'm admin!")
        return
    
    # Create group selection buttons
    keyboard = []
    for group_id, group_info in bot_data.groups_info.items():
        is_selected = group_id in bot_data.selected_groups
        emoji = "✅" if is_selected else "◻️"
        keyboard.append([
            InlineKeyboardButton(
                f"{group_info['name']} {emoji}",
                callback_data=f"toggle_group:{group_id}"
            )
        ])
    
    # Add control buttons
    keyboard.append([
        InlineKeyboardButton("🔘 Select All", callback_data="select_all_groups"),
        InlineKeyboardButton("🚀 Send", callback_data="proceed_to_forward")
    ])
    
    await query.edit_message_text(
        "👇 Select Groups to Forward Messages:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def toggle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    group_id = int(query.data.split(":")[1])
    
    # Toggle selection
    if group_id in bot_data.selected_groups:
        bot_data.selected_groups.remove(group_id)
    else:
        bot_data.selected_groups.add(group_id)
    
    # Refresh the group list
    await select_groups(update, context)

async def select_all_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Select all available groups
    bot_data.selected_groups = set(bot_data.groups_info.keys())
    await select_groups(update, context)

def setup_callbacks(application):
    application.add_handler(CallbackQueryHandler(select_groups, pattern="^select_groups$"))
    application.add_handler(CallbackQueryHandler(toggle_group, pattern="^toggle_group:"))
    application.add_handler(CallbackQueryHandler(select_all_groups, pattern="^select_all_groups$"))
    application.add_handler(CallbackQueryHandler(proceed_to_forward, pattern="^proceed_to_forward$"))
