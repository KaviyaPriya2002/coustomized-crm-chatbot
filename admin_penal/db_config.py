from pymongo import MongoClient

Client = MongoClient("mongodb://localhost:27017/")
db = Client['new_product']
collection = db['super admin']
sub_admins = db['sub_admins']
create_bot = db['create_bot']
Intents = db["Intents"]
contact_form=db["contact_details"]
faq_questions = db["faq_questions"]
chatbot_flow = db["chatbot_flow"]

def get_db():
    return create_bot