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
    
    # Fetch groups if not already done
    if not bot_data.groups_info:
        await bot_data.fetch_groups(context)
    
    if not bot_data.groups_info:
        await query.edit_message_text(
            "❌ No groups found where I'm admin!\n"
            "Please add me to groups and make me admin first."
        )
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
    control_buttons = []
    if bot_data.groups_info:
        control_buttons.append(
            InlineKeyboardButton("Select All", callback_data="select_all_groups")
        )
        control_buttons.append(
            InlineKeyboardButton("Deselect All", callback_data="deselect_all_groups")
        )
    
    if control_buttons:
        keyboard.append(control_buttons)
    
    # Add proceed button if groups selected
    if bot_data.selected_groups:
        keyboard.append([
            InlineKeyboardButton("Proceed to Topics ➡️", callback_data="proceed_to_topics")
        ])
    
    await query.edit_message_text(
        "👥 Select Groups to Forward:",
        reply_markup=InlineKeyboardMarkup(keyboard)
