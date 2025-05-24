from typing import Dict, List, Set, Optional
from telegram import Chat

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
        self.selected_groups: Set[int] = set()
        self.selected_topics: Dict[int, Set[int]] = {}
        self.messages_to_forward: List[Dict] = []
        self.groups_info: Dict[int, Dict] = {}

    async def fetch_groups(self, context):
        """Fetch all groups where bot is admin"""
        self.groups_info = {}
        if not Config.GROUP_IDS:
            return
            
        for group_id in Config.GROUP_IDS:
            try:
                chat = await context.bot.get_chat(group_id)
                # Check if bot is admin
                member = await context.bot.get_chat_member(group_id, context.bot.id)
                if member.status in ['administrator', 'creator']:
                    self.groups_info[group_id] = {
                        'name': chat.title,
                        'topics': {}
                    }
            except Exception as e:
                print(f"Error fetching group {group_id}: {e}")

bot_data = BotData()
