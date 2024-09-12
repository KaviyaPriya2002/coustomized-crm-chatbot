from admin_penal.db_config import faq_questions
from datetime import datetime
from bson import ObjectId

class FAQ:
    def __init__(self, question=None, answer=None):
        self.question = question
        self.answer = answer
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        result = faq_questions.insert_one({
            'question': self.question,
            'answer': self.answer,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        })
        return str(result.inserted_id)

    def create_faq(self, faq_data):
        faq = {
            'question': faq_data['question'],
            'answer': faq_data['answer'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = faq_questions.insert_one(faq)
        return str(result.inserted_id)

    def update_faq(self, faq_id, update_data):
        # Update an existing FAQ by ID
        update_data['updated_at'] = datetime.utcnow()  # Automatically update the timestamp
        result = faq_questions.update_one({'_id': ObjectId(faq_id)}, {'$set': update_data})
        return result.modified_count  # Returns the number of documents modified

    def delete_faq(self, faq_id):
        # Delete an FAQ by ID
        result = faq_questions.delete_one({'_id': ObjectId(faq_id)})
        return result.deleted_count  # Returns the number of documents deleted

    def get_all_faqs(self):
        faqs = faq_questions.find({})
        # Convert ObjectId to string for each FAQ
        return [{**faq, "_id": str(faq["_id"])} for faq in faqs]

    def get_faq_by_id(self, faq_id):
        faq = faq_questions.find_one({'_id': ObjectId(faq_id)})
        if faq:
            faq["_id"] = str(faq["_id"])  # Convert ObjectId to string
        return faq