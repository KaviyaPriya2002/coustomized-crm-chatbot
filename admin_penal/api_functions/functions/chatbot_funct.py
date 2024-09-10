from admin_penal.db_config import Intents

def insert_template(template_data):

    Intent = Intents.insert_one(template_data)
