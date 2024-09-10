from admin_penal.db_config import collection,db
from bson import ObjectId


class super_admin:
    def __init__(self, adminname, email, phone_number, password,role):
        self.adminname = adminname
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.role = role

    def save(self):
        result = collection.insert_one({
            'adminname': self.adminname,
            'email': self.email,
            'phone_number': self.phone_number,
            'password': self.password,
            'role' : self.role
        })
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        return collection.find_one({'email': email})
