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
        self.selected_groups = set()  # Initialize as empty set
        self.groups_info = {}  # Stores group info
        
    async def fetch_groups(self, context):
        """Fetch groups where bot is admin"""
        self.groups_info = {}
        for group_id in Config.GROUP_IDS:
            try:
                chat = await context.bot.get_chat(group_id)
                member = await context.bot.get_chat_member(group_id, context.bot.id)
                if member.status in ['administrator', 'creator']:
                    self.groups_info[group_id] = {
                        'name': chat.title,
                        'topics': {}
                    }
            except Exception as e:
                logger.error(f"Error fetching group {group_id}: {e}")
