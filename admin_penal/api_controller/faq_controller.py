from flask import Blueprint, request, jsonify
from admin_penal.api_functions.models.faq_model import FAQ
from marshmallow import ValidationError
from admin_penal.api_functions.schemas.faq_schema import FAQSchema
from admin_penal.db_config import faq_questions
from admin_penal.api_functions.functions.admin_func import is_authenticated

faq_bp = Blueprint('faq_bp', __name__)
faq_service = FAQ()


@faq_bp.route('/add-faq', methods=['POST'])
@is_authenticated('super-admin')
def add_faq(admin):
    try:
        data = request.get_json()
        faq_schema = FAQSchema(many=True)  # Specify many=True for multiple FAQ objects
        faq_data = faq_schema.load(data)  # Load and validate multiple FAQs
        faqs = faq_service.create_faqs(faq_data)  # Process the array of FAQs

        return jsonify({"message": "FAQs added successfully", "faqs": faqs}), 200
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400


@faq_bp.route('/get-faqs', methods=['GET'])
def get_all():
    # Fetch the document containing all FAQs
    faq_document = faq_service.get_faq_document()
    print("faq_document",faq_document)

    # Extract the 'faqs' array from the document
    if faq_document and 'faqs' in faq_document:
        faqs = faq_document['faqs']
    else:
        faqs = []

    # Convert ObjectId to string for serialization
    for faq in faqs:
        faq['id'] = str(faq['id'])

    # Prepare the response data
    response_data = {
        'success': True,
        'total_faqs': len(faqs),  # Total number of FAQs
        'faq_list': faqs
    }

    print("response_data", response_data)
    return jsonify(response_data)


@faq_bp.route('/faqs/<string:faq_id>', methods=['GET'])
def get_faq_by_id(faq_id):
    faq = faq_service.get_faq_by_id(faq_id)
    if faq:
        return jsonify(faq), 200
    else:
        return jsonify({"message": "FAQ not found"}), 404

@faq_bp.route('/edit-faqs/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    try:
        data = request.get_json()
        faq_schema = FAQSchema(partial=True)
        validated_data = faq_schema.load(data)
        if faq_service.update_faq(faq_id, validated_data):
            return jsonify({"message": "FAQ updated successfully"}), 200
        else:
            return jsonify({"message": "FAQ not found"}), 404
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

@faq_bp.route('/delete-faqs/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    if faq_service.delete_faq(faq_id):
        return jsonify({"message": "FAQ deleted successfully"}), 200
    else:
        return jsonify({"message": "FAQ not found"}), 404
