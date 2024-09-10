from admin_penal.db_config import create_bot

def insert_bot(chatbot_data):
    result = create_bot.insert_one(chatbot_data)
    # print("result************",result)
    inserted_id = result.inserted_id
    # print("insert id@@@@@@@@@@@@@@@@@@@",inserted_id)
    inserted_data = create_bot.find_one({"_id": inserted_id})  # Retrieve inserted data
    # print("Inserted data:")
    print(inserted_data)  # Print the full data that was inserted
    return {'inserted_data': str(inserted_data)}
