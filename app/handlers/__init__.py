from app.handlers.commands import setup_commands
from app.handlers.messages import setup_messages

def setup_handlers(application):
    setup_commands(application)
    setup_messages(application)
