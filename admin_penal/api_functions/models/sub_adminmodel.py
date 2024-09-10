from admin_penal.db_config import sub_admins

class User:
    def __init__(self, username, email, phone_number, password,role):
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.role = role

    def save(self):
        result = sub_admins.insert_one({
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'password': self.password,
            'role': self.role
        })
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        return sub_admins.find_one({'email': email})
