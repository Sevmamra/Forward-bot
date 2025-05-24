from typing import Dict, List, Set, Optional

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

bot_data = BotData()
