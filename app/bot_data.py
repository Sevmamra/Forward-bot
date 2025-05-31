import logging

logger = logging.getLogger(__name__)

class BotData:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.collecting = False
        self.messages_to_forward = []

bot_data = BotData()
