from telegram.error import TelegramError
from telegram.constants import ParseMode
import logging

logger = logging.getLogger(__name__)

async def fetch_topics(bot, chat_id):
    """Fetch topics with error handling"""
    try:
        forum = await bot.get_forum_topics(chat_id)
        return {topic.message_thread_id: topic.name for topic in forum.topics}
    except TelegramError as e:
        logger.error(f"Topics fetch failed: {e}")
        return {}

async def create_topic(bot, chat_id, name):
    """Create topic with error handling"""
    try:
        topic = await bot.create_forum_topic(
            chat_id=chat_id,
            name=name,
            icon_color=0x6FB9F0
        )
        return topic.message_thread_id
    except TelegramError as e:
        logger.error(f"Topic creation failed: {e}")
        return None
