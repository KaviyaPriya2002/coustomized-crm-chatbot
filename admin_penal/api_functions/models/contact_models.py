from admin_penal.db_config import contact_form
from datetime import datetime

class Contact_details:
    def __init__(self, name, email, phone_number, message):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.message = message
        self.created_at = datetime.utcnow()



    def save(self):
        result = contact_form.insert_one({
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'message': self.message,
            'created_at': self.created_at,


        })
        return str(result.inserted_id)