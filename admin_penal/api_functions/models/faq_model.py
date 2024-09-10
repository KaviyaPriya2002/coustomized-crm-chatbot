from datetime import datetime
from bson import ObjectId
from admin_penal.db_config import faq_questions


class FAQ:
    def __init__(self):
        self.collection = faq_questions

    def get_faq_document(self):
        # Assuming there's only one document holding all FAQs
        faq_document = self.collection.find_one()
        if faq_document:
            faqs = faq_document.get('faqs', [])
            for faq in faqs:
                faq['_id'] = str(faq.get('id'))
        return faq_document

    def create_faqs(self, faqs):
        # Get the current FAQs
        faq_document = self.get_faq_document()
        existing_faqs = faq_document.get('faqs', []) if faq_document else []

        # Determine the next ID
        existing_ids = {faq.get('id') for faq in existing_faqs}
        next_id = 1
        while next_id in existing_ids:
            next_id += 1

        # Assign unique IDs to new FAQs
        for faq in faqs:
            faq.update({
                'id': next_id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            next_id += 1

        # Update the document with the new FAQs
        if faq_document:
            result = self.collection.update_one(
                {},
                {'$push': {'faqs': {'$each': faqs}}},
                upsert=True
            )
        else:
            result = self.collection.insert_one({'faqs': faqs})
        return faqs

    def update_faq(self, faq_id, updated_data):
        faq_document = self.get_faq_document()
        if faq_document:
            faqs = faq_document.get('faqs', [])
            for faq in faqs:
                if faq.get('id') == faq_id:
                    faq.update(updated_data)
                    faq['updated_at'] = datetime.utcnow()
                    self.collection.update_one(
                        {},
                        {'$set': {'faqs': faqs}}
                    )
                    return True
        return False

    def delete_faq(self, faq_id):
        faq_document = self.get_faq_document()
        if faq_document:
            faqs = faq_document.get('faqs', [])
            updated_faqs = [faq for faq in faqs if faq.get('id') != faq_id]
            if len(faqs) != len(updated_faqs):
                self.collection.update_one(
                    {},
                    {'$set': {'faqs': updated_faqs}}
                )
                return True
        return False