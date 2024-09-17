from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from user.api_functions.models.chatbot_model import Bot_details
from user.api_functions.schemas.chatbot_schema import CreateBot
from flask_cors import CORS
from admin_penal.api_functions.functions.sub_adminfunct import is_subadmin
from admin_penal.db_config import create_bot

bot_bp = Blueprint('bot_bp', __name__)
CORS(bot_bp)

@bot_bp.route('/add-chatbot', methods=['POST'])
@is_subadmin('user')
def add_chatbot(user):
    try:
        data = request.get_json()
        print("data////////....",data)
        # This will now handle a single FAQ entry
        bot_schema = CreateBot()  # Handle single FAQ
        bot_data = bot_schema.load(data)  # Validate the single FAQ entry

        # Create and save the FAQ using the dynamic FAQ model
        chatbot_service = Bot_details()
        bot_id = chatbot_service.create_bot(bot_data)
        bot_response_data = bot_schema.dump(bot_data)
        print("bot-data>>>>", bot_response_data)

        return jsonify({"message": "bot created successfully", "bot_id": bot_id, "success": True, "status code": 200,"bot_data":bot_response_data}), 200
    except ValidationError as err:
        return jsonify({"errors": err.messages, "success": False, "status code": 400}), 400

