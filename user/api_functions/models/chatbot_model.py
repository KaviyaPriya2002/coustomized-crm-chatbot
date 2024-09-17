from admin_penal.db_config import create_bot
from datetime import datetime

class Bot_details:
    def __init__(self, bot_name=None, description=None,bot_type=None):
        self.bot_name = bot_name
        self.description = description
        self.bot_type =bot_type
        self.created_at = datetime.utcnow()


    def save(self):
        result = create_bot.insert_one({
            'bot_name': self.bot_name,
            'description': self.description,
            "bot_type":self.bot_type,
            'created_at': self.created_at,



        })
        return str(result.inserted_id)
    def create_bot(self, bot_data):
        chatbot = {
            'bot_name': bot_data['bot_name'],
            'description': bot_data['description'],
            "bot_type": bot_data['bot_type'],
            'created_at': datetime.utcnow()
        }
        result = create_bot.insert_one(chatbot)
        return str(result.inserted_id)