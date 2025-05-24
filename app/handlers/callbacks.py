from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from app.config import Config
from app.bot_data import bot_data

async def start_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    bot_data.reset()
    bot_data.collecting = True
    await query.edit_message_text("📤 Send me videos, files, text messages etc.\nWhen finished, send /done command")

async def select_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
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
    
    keyboard.append([
        InlineKeyboardButton("Select All", callback_data="select_all_groups"),
        InlineKeyboardButton("Deselect All", callback_data="deselect_all_groups")
    ])
    
    keyboard.append([InlineKeyboardButton("Proceed to Topics ➡️", callback_data="confirm_send")])
    
    await query.edit_message_text(
        "👥 Select Groups to Forward:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def setup_callbacks(application):
    application.add_handler(CallbackQueryHandler(start_process, pattern="^start_process$"))
    application.add_handler(CallbackQueryHandler(select_groups, pattern="^select_groups$"))
