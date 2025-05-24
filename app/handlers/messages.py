from telegram.ext import MessageHandler, filters
from config import Config
from app.bot_data import bot_data

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all non-command messages."""
    if not bot_data.collecting or update.effective_user.id != Config.AUTHORIZED_USER_ID:
        return

    # Count and store messages for forwarding
    message = update.message
    if message.video:
        bot_data.received_items['videos'] += 1
    elif message.document:
        bot_data.received_items['files'] += 1
    elif message.photo:
        bot_data.received_items['photos'] += 1
    elif message.text and not message.text.startswith('/'):
        bot_data.received_items['texts'] += 1
    else:
        bot_data.received_items['others'] += 1

    # Store message data
    msg_data = {
        'message': message,
        'type': 'video' if message.video else 
               'document' if message.document else 
               'photo' if message.photo else 
               'text',
        'content': message.video or message.document or 
                  (message.photo[-1] if message.photo else None) or 
                  message.text,
        'caption': message.caption,
        'entities': message.entities or message.caption_entities
    }
    bot_data.messages_to_forward.append(msg_data)

def setup_messages(application):
    """Register message handlers."""
    application.add_handler(MessageHandler(
        filters.ChatType.PRIVATE & 
        ~filters.COMMAND & 
        (filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL),
        handle_message
    ))
