from flask import Blueprint, request, jsonify
from admin_penal.db_config import chatbot_flow, intents_collection  # Import your MongoDB collections
from bson import ObjectId
from user.api_functions.functions.convertflow_function import convert_flow_to_intents

intent_bp = Blueprint('intent_bp', __name__)


@intent_bp.route('/api/convert-flow', methods=['POST'])
def convert_flow():
    try:
        # Extract chatbot_id from the request
        data = request.get_json()
        chatbot_id = data.get('chatbot_id')
        if not chatbot_id:
            return jsonify({"message": "chatbot_id is required", "success": False}), 400

        # Retrieve the chatbot flow data from the database
        chatbot_flow_data = chatbot_flow.find_one({"chatbot_id": ObjectId(chatbot_id)})

        if not chatbot_flow_data:
            return jsonify({"message": "No flow data found for the provided chatbot_id", "success": False}), 404

        # Convert flow data to the intents format
        intents_data = convert_flow_to_intents(chatbot_flow_data)

        # Store the intents data in the database
        intents_data_to_store = {
            "chatbot_id": ObjectId(chatbot_id),
            "intents": intents_data["intents"]
        }
        intents_collection.insert_one(intents_data_to_store)

        return jsonify({
            "message": "Flow successfully converted and stored as intents",
            "intents": intents_data,
            "success": True,
            "status_code": 200
        }), 200
    except Exception as e:
        return jsonify({
            "message": str(e),
            "success": False,
            "status_code": 500
        }), 500