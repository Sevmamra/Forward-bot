from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from app.config import Config
from app.bot_data import bot_data

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.AUTHORIZED_USER_ID:
        return

    welcome_msg = (
        f"ʜᴇʟʟᴏ, {update.effective_user.full_name} ꜱɪʀ!\n\n"
        "ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴏᴜʀ ꜰᴏʀᴡᴀʀᴅɪɴɢ ʙᴏᴛ ꜱᴇʀᴠɪᴄᴇ.\n\n"
        "ꜱɪᴍᴘʟʏ ꜱᴇɴᴅ ᴀɴʏ ᴍᴇꜱꜱᴀɢᴇ, ᴘʜᴏᴛᴏ, ᴠɪᴅᴇᴏ, ᴅᴏᴄᴜᴍᴇɴᴛ, ᴏʀ ꜰɪʟᴇ ʜᴇʀᴇ — ᴀɴᴅ ᴏᴜʀ ʙᴏᴛ ᴡɪʟʟ ɪɴꜱᴛᴀɴᴛʟʏ ꜰᴏʀᴡᴀʀᴅ ɪᴛ ᴛᴏ ʏᴏᴜʀ ᴅᴇꜱɪɢɴᴀᴛᴇᴅ ɢʀᴏᴜᴘ, ᴇɴꜱᴜʀɪɴɢ ꜱᴇᴀᴍʟᴇꜱꜱ ᴀɴᴅ ᴇꜰꜰɪᴄɪᴇɴᴛ ᴅᴇʟɪᴠᴇʀʏ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴅᴇʟᴀʏ.\n\n"
        "ᴍᴀᴅᴇ ᴡɪᴛʜ ❤️ ʙʏ 𝐂𝐀 𝐈𝐧𝐭𝐞𝐫 𝐗"
    )

    keyboard = [[InlineKeyboardButton("Start Process", callback_data="start_process")]]
    await update.message.reply_text(welcome_msg, reply_markup=InlineKeyboardMarkup(keyboard))

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.AUTHORIZED_USER_ID:
        return

    bot_data.collecting = False
    
    report = (
        "📊 Received Items Summary:\n\n"
        f"🎬 Videos: {bot_data.received_items['videos']}\n"
        f"📁 Files: {bot_data.received_items['files']}\n"
        f"🖼️ Photos: {bot_data.received_items['photos']}\n"
        f"📝 Texts: {bot_data.received_items['texts']}\n"
        f"📦 Others: {bot_data.received_items['others']}\n\n"
        f"🔢 Total: {sum(bot_data.received_items.values())}"
    )
    
    # Ensure groups are loaded
    if not bot_data.groups_info:
        await bot_data.fetch_groups(context)
    
    keyboard = [[InlineKeyboardButton("SELECT GROUPS", callback_data="select_groups")]]
    await update.message.reply_text(report, reply_markup=InlineKeyboardMarkup(keyboard))
