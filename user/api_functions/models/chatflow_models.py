from bson import ObjectId
from admin_penal.db_config import chatbot_flow  # Import your DB collection
from datetime import datetime

class FlowDetails:
    def __init__(self, chatbot_id, nodes, edges):
        self.chatbot_id = ObjectId(chatbot_id)
        self.nodes = nodes
        self.edges = edges

    def save(self):
        flow_data =chatbot_flow.insert_one ({
            "chatbot_id": self.chatbot_id,
            "nodes": self.nodes,
            "edges": self.edges
        })
        return str(flow_data.inserted_id)

    def create_flow(self, bot_flow):
        chatbot = {
            'chatbot_id': ObjectId(bot_flow['chatbot_id']),
            'nodes': bot_flow['nodes'],
            "edges": bot_flow['edges'],
            'created_at': datetime.utcnow()
        }
        result = chatbot_flow.insert_one(chatbot)
        return str(result.inserted_id)

    def update_flow(self, faq_id, update_data):
        # Update an existing FAQ by ID
        update_data['created_at'] = datetime.utcnow()  # Automatically update the timestamp
        result = chatbot_flow.update_one({'_id': ObjectId(faq_id)}, {'$set': update_data})
        return result.modified_count
