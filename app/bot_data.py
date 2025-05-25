from typing import Dict, List, Set, Optional
from telegram import Chat
from app.config import Config
import logging

logger = logging.getLogger(__name__)

class BotData:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.received_items = {
            'videos': 0,
            'files': 0,
            'texts': 0,
            'photos': 0,
            'others': 0
        }
        self.collecting = False
        self.selected_groups: Dict[int, Set[int]] = {}  # {group_id: set(topic_ids)}
        self.messages_to_forward: List[Dict] = []
        self.groups_info: Dict[int, Dict] = {}

    async def fetch_topics(self, context, group_id):
        """Fetch topics for a specific group"""
        try:
            chat = await context.bot.get_chat(group_id)
            if chat.is_forum:
                self.groups_info[group_id]['topics'] = {
                    # Default general topic
                    1: "General"  
                }
                # Add your logic to fetch existing topics here
        except Exception as e:
            logger.error(f"Error fetching topics for {group_id}: {e}")

bot_data = BotData()
