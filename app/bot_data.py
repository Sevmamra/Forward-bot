import logging
from app.config import Config

logger = logging.getLogger(__name__)

class BotData:
    def __init__(self):
        self.reset()

    def reset(self):
        self.collecting = False
        self.messages_to_forward = []
        self.received_items = {
            'videos': 0,
            'files': 0,
            'photos': 0,
            'texts': 0,
            'others': 0
        }
        self.groups_info = {}
        self.selected_groups = {}

    async def fetch_groups(self, context):
        try:
            for group_id in Config.GROUP_IDS:
                chat = await context.bot.get_chat(group_id)
                self.groups_info[group_id] = {
                    'name': chat.title,
                    'topics': {}
                }
        except Exception as e:
            logger.error(f"Failed to fetch groups: {e}")

    async def fetch_topics(self, context, group_id):
        try:
            topics = await context.bot.get_forum_topic_list(group_id)
            self.groups_info[group_id]['topics'] = {
                topic.message_thread_id: topic.name
                for topic in topics
            }

            # Agar group ke topics abhi tak selected_groups me nahi hai to default me sab add kar do
            if group_id not in self.selected_groups:
                self.selected_groups[group_id] = set(self.groups_info[group_id]['topics'].keys())

        except Exception as e:
            logger.error(f"Failed to fetch topics for group {group_id}: {e}")

bot_data = BotData()
