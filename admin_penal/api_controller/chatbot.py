from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from admin_penal.api_functions.functions.chatbot_funct import insert_template
from admin_penal.api_functions.schemas.chatbot_schema import template_schema

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/api/templates', methods=['POST'])
def create_template():
    print("create_template>>>>>>",create_template)
    try:
        data = template_schema.load(request.json)
        print("data",data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    insert_template(data)
    return jsonify({"message": "Template created successfully"}), 200
