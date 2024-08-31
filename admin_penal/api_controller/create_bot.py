
from admin_penal.api_functions.functions.create_botfunct import create_botfunt, is_createchat
from admin_penal.api_functions.schemas.createbot_schemas import CreatebotSchema
from admin_penal.db_config import create_bot
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from bson import ObjectId

createchat_bp = Blueprint('create_chat', __name__)
createbot_schema = CreatebotSchema()


@createchat_bp.route('/create_chatbot', methods=['POST'])
@is_createchat
def create_chatbot_endpoint(user):
    data = request.get_json()
    print("data",data)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        validated_data = createbot_schema.load(data)
        print("validate_data",validated_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    result = create_botfunt(validated_data, user) # Pass the user to the create_bot function
    print("result>>>>>>>>",result)
    return jsonify({"message": "Chatbot created successfully", "success": True, "result": result}), 200


@createchat_bp.route('/edit_chatbot/<string:bot_id>', methods=['PUT'])
def edit_chatbot(bot_id):
    data = request.get_json()
    print("data", data)

    # Convert sets to lists in the data
    for key, value in data.items():
        if isinstance(value, set):
            data[key] = list(value)

    try:
        result = create_bot.update_one({'_id': ObjectId(bot_id)}, {'$set': data})

        if result.matched_count > 0:
            return jsonify({'message': 'Chatbot updated successfully'}), 200
        else:
            return jsonify({'message': 'Chatbot not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@createchat_bp.route('/delete_bot/<string:chat_id>', methods=["DELETE"])
def delete_package(chat_id):
    try:
        result = create_bot.delete_one({'_id': ObjectId(chat_id)})
        if result.deleted_count > 0:
            return jsonify({"message": "chatbot deleted successfully"}), 200
        else:
            return jsonify({"message": "chatbot not found"}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400
