from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from user.api_functions.models.chatflow_models import FlowDetails  # Ensure this is the correct model
from user.api_functions.schemas.chatflow_schema import create_dynamic_flow_schema
from flask_cors import CORS
from admin_penal.db_config import create_bot

flow_bp = Blueprint('flow_bp', __name__)
CORS(flow_bp)


@flow_bp.route('/create-flow', methods=['POST'])
def add_chatflow():
    try:
        data = request.get_json()
        chatbot_id = data.get('chatbot_id')  # Retrieve chatbot_id from the request
        if not chatbot_id:
            return jsonify({"message": "chatbot_id is required", "success": False}), 400

        # Create schema dynamically using chatbot_id
        bot_schema = create_dynamic_flow_schema()

        # Validate the data using the schema
        bot_data = bot_schema.load(data)

        # Retrieve nodes and edges from validated data
        nodes = bot_data.get('nodes')
        edges = bot_data.get('edges')


        for i, node in enumerate(nodes):
            if 'id' not in node or not node['id']:
                node['id'] = f"node_{i + 1}"

        # Create and save the flow using the dynamic model
        chatbotflow_service = FlowDetails(chatbot_id=chatbot_id, nodes=nodes, edges=edges)  # Pass required arguments
        bot_id = chatbotflow_service.create_flow(bot_data)  # Call the save method to insert the data
        bot_response_data = bot_schema.dump(bot_data)
        print("bot-data>>>>", bot_response_data)

        return jsonify({
            "message": "Chatflow created successfully",
            "bot_id": str(bot_id),
            "success": True,
            "status_code": 200,
            "bot_data": bot_response_data
        }), 200
    except ValidationError as err:
        return jsonify({
            "errors": err.messages,
            "success": False,
            "status_code": 400
        }), 400
    except Exception as e:
        return jsonify({
            "message": str(e),
            "success": False,
            "status_code": 500
        }), 500


@flow_bp.route('/update-flow/<flow_id>', methods=['PUT'])
def update_flow(flow_id):
    try:
        data = request.get_json()

        # Create the schema without 'partial'
        flow_schema = create_dynamic_flow_schema()

        # Validate the input data for partial updates by passing 'partial=True' to the load method
        update_data = flow_schema.load(data, partial=True)
        print("update_data >>>>>>", update_data)

        # Retrieve chatbot_id if it exists in the update data
        chatbot_id = update_data.get('chatbot_id')
        # if not chatbot_id:
        #     return jsonify({"message": "chatbot_id is required", "success": False}), 400

        # Retrieve nodes and edges from the data
        nodes = update_data.get('nodes', [])
        edges = update_data.get('edges', [])

        # Assign unique IDs to nodes if not present
        for i, node in enumerate(nodes):
            if 'id' not in node or not node['id']:
                node['id'] = f"node_{i + 1}"

        # Initialize the service to update the flow
        flow_service = FlowDetails(chatbot_id=chatbot_id, nodes=nodes, edges=edges)
        modified_count = flow_service.update_flow(flow_id, update_data)  # Call the appropriate update method

        if modified_count > 0:
            return jsonify({"message": "Flow updated successfully", "success": True, "status_code": 200}), 200
        else:
            return jsonify({"message": "Flow not found or no changes made", "success": False, "status_code": 404}), 404
    except ValidationError as err:
        return jsonify({"errors": err.messages, "success": False, "status_code": 400}), 400
    except Exception as e:
        return jsonify({"message": str(e), "success": False, "status_code": 500}), 500
