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
    
    if not bot_data.groups_info:
        await bot_data.fetch_groups(context)
    
    if not bot_data.groups_info:
        await query.edit_message_text("❌ No groups found where I'm admin!")
        return
    
    keyboard = []
    for group_id, group_info in bot_data.groups_info.items():
        is_selected = group_id in bot_data.selected_groups
        emoji = "✅" if is_selected else "◻️"  # YOUR TOGGLE ICONS
        keyboard.append([
            InlineKeyboardButton(
                f"{group_info['name']} {emoji}",  # SHOWS NAME WITH EMOJI
                callback_data=f"toggle_group:{group_id}"
            )
        ])
    
    # ADD CONTROL BUTTONS
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
    
    # TOGGLE SELECTION WITH ✅/◻️
    if group_id in bot_data.selected_groups:
        bot_data.selected_groups.remove(group_id)
    else:
        bot_data.selected_groups.add(group_id)
    
    # REFRESH THE LIST
    await select_groups(update, context)

async def select_all_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    bot_data.selected_groups = set(bot_data.groups_info.keys())
    await select_groups(update, context)

async def proceed_to_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not bot_data.selected_groups:
        await query.edit_message_text("❌ No groups selected!")
        return
    
    success_count = 0
    for msg_data in bot_data.messages_to_forward:
        for group_id in bot_data.selected_groups:
            try:
                if msg_data['type'] == 'video':
                    await context.bot.send_video(
                        chat_id=group_id,
                        video=msg_data['content'],
                        caption=msg_data.get('caption')
                    )
                elif msg_data['type'] == 'photo':
                    await context.bot.send_photo(
                        chat_id=group_id,
                        photo=msg_data['content'],
                        caption=msg_data.get('caption')
                    )
                elif msg_data['type'] == 'document':
                    await context.bot.send_document(
                        chat_id=group_id,
                        document=msg_data['content'],
                        caption=msg_data.get('caption')
                    )
                elif msg_data['type'] == 'text':
                    await context.bot.send_message(
                        chat_id=group_id,
                        text=msg_data['content']
                    )
                success_count += 1
            except Exception as e:
                logger.error(f"Forward failed to {group_id}: {e}")
    
    await query.edit_message_text(
        f"✅ Forwarded {success_count} items to {len(bot_data.selected_groups)} groups!"
    )
    bot_data.reset()

def setup_callbacks(application):
    application.add_handler(CallbackQueryHandler(start_process, pattern="^start_process$"))
    application.add_handler(CallbackQueryHandler(select_groups, pattern="^select_groups$"))
    application.add_handler(CallbackQueryHandler(toggle_group, pattern="^toggle_group:"))
    application.add_handler(CallbackQueryHandler(select_all_groups, pattern="^select_all_groups$"))
    application.add_handler(CallbackQueryHandler(proceed_to_forward, pattern="^proceed_to_forward$"))
