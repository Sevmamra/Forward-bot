class BotData:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.received_items = {
            'videos': 0,
            'files': 0,
            'texts': 0,
            'photos': 0
        }
        self.collecting = False
        self.selected_groups = set()
        self.messages_to_forward = []

# Create the shared instance
bot_data = BotData()
