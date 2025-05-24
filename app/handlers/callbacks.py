from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from app.config import Config
from app.bot_data import bot_data
import logging

logger = logging.getLogger(__name__)

async def start_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    bot_data.reset()
    bot_data.collecting = True
    await query.edit_message_text("📤 Send me videos, files, text messages etc.\nWhen finished, send /done command")

async def select_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # First fetch groups if not already done
    if not bot_data.groups_info:
        await bot_data.fetch_groups(context)
    
    if not bot_data.groups_info:
        await query.edit_message_text("❌ No groups found where I'm admin!")
        return
    
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
        InlineKeyboardButton("Select All", callback_data="select_all_groups"),
        InlineKeyboardButton("Deselect All", callback_data="deselect_all_groups")
    ])
    
    # Add proceed button if groups selected
    if bot_data.selected_groups:
        keyboard.append([
            InlineKeyboardButton("Proceed to Topics ➡️", callback_data="proceed_to_topics")
        ])
    
    await query.edit_message_text(
        "👥 Select Groups to Forward:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def toggle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    group_id = int(query.data.split(':')[1])
    
    if group_id in bot_data.selected_groups:
        bot_data.selected_groups.remove(group_id)
    else:
        bot_data.selected_groups.add(group_id)
    
    # Refresh the group selection menu
    await select_groups(update, context)

async def proceed_to_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not bot_data.selected_groups:
        await query.answer("Please select at least one group!", show_alert=True)
        return
    
    # Implement topic selection logic here
    await query.edit_message_text("Topics selection will be implemented next")

def setup_callbacks(application):
    application.add_handler(CallbackQueryHandler(start_process, pattern="^start_process$"))
    application.add_handler(CallbackQueryHandler(select_groups, pattern="^select_groups$"))
    application.add_handler(CallbackQueryHandler(toggle_group, pattern="^toggle_group:"))
    application.add_handler(CallbackQueryHandler(proceed_to_topics, pattern="^proceed_to_topics$"))
