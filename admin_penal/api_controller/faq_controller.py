from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from admin_penal.api_functions.models.faq_model import FAQ
from admin_penal.api_functions.schemas.faq_schema import FAQSchema
from admin_penal.api_functions.functions.admin_func import is_authenticated
from flask_cors import CORS

from admin_penal.db_config import faq_questions

faq_bp = Blueprint('faq_bp', __name__)
CORS(faq_bp)

@faq_bp.route('/super_admin/add-faq', methods=['POST'])
@is_authenticated('super-admin')
def add_faq(admin):
    try:
        data = request.get_json()  # This will now handle a single FAQ entry
        faq_schema = FAQSchema()  # Handle single FAQ
        faq_data = faq_schema.load(data)  # Validate the single FAQ entry

        # Create and save the FAQ using the dynamic FAQ model
        faq_service = FAQ()
        faq_id = faq_service.create_faq(faq_data)

        return jsonify({"message": "FAQ added successfully", "faq_id": faq_id, "success": True, "status code": 200}), 200
    except ValidationError as err:
        return jsonify({"errors": err.messages, "success": False, "status code": 400}), 400

@faq_bp.route('/super_admin/update-faq/<faq_id>', methods=['PUT'])
@is_authenticated('super-admin')
def update_faq(admin, faq_id):
    try:
        data = request.get_json()
        faq_schema = FAQSchema(partial=True)  # Allow partial updates (only provided fields)
        update_data = faq_schema.load(data)
        print("upsater >>>>>>",update_data)

        faq_service = FAQ()
        modified_count = faq_service.update_faq(faq_id, update_data)
        print("mofigied<<<<<<<<<<<<<<",modified_count)

        if modified_count > 0:

            return jsonify({"message": "FAQ updated successfully", "success": True, "status code": 200}), 200
        else:
            return jsonify({"message": "FAQ not found or no changes made", "success": False, "status code": 404}), 404
    except ValidationError as err:
        return jsonify({"errors": err.messages, "success": False, "status code": 400}), 400
@faq_bp.route('/super_admin/delete-faq/<faq_id>', methods=['DELETE'])
@is_authenticated('super-admin')
def delete_faq(admin, faq_id):
    faq_service = FAQ()
    deleted_count = faq_service.delete_faq(faq_id)

    if deleted_count > 0:
        return jsonify({"message": "FAQ deleted successfully", "success": True, "status code": 200}), 200
    else:
        return jsonify({"message": "FAQ not found", "success": False, "status code": 404}), 404
@faq_bp.route('/super_admin/get-all-faqs', methods=['GET'])
@is_authenticated('super-admin')
def get_all_faqs(admin):
    faq_service = FAQ()
    faqs = faq_service.get_all_faqs()

    return jsonify({"faqs": faqs, "success": True, "status code": 200}), 200

@faq_bp.route('/super_admin/get-faq/<faq_id>', methods=['GET'])
@is_authenticated('super-admin')
def get_faq(admin, faq_id):
    faq_service = FAQ()
    faq = faq_service.get_faq_by_id(faq_id)

    if faq:
        return jsonify({"faq": faq, "success": True, "status code": 200}), 200
    else:
        return jsonify({"message": "FAQ not found", "success": False, "status code": 404}), 404


# @faq_bp.route('/super_admin/delete-faq/<faq_id>', methods=['DELETE'])
# @is_authenticated('super-admin')
# def delete_faq_by_id(admin, faq_id):  # Rename the function here
#     faq_service = FAQ()
#     deleted_count = faq_service.delete_faq(faq_id)
#
#     if deleted_count > 0:
#         return jsonify({"message": "FAQ deleted successfully", "success": True, "status code": 200}), 200
#     else:
#         return jsonify({"message": "FAQ not found", "success": False, "status code": 404}), 404

