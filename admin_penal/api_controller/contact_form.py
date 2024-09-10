from flask import Blueprint, request, jsonify,make_response
from marshmallow import ValidationError
from admin_penal.api_functions.models.contact_models import Contact_details
from admin_penal.api_functions.schemas.contact_schema import ContactForm
from flask_cors import CORS
from admin_penal.db_config import contact_form
from bson import ObjectId


contact_bp = Blueprint('contact_details', __name__)
CORS(contact_bp)
@contact_bp.route('/contact_form/create', methods=['POST'])
def contact_details():
    response_data = {
        'success': False,  # Default to False
        'message': 'An error occurred',  # Default message
    }
    data = request.get_json()
    schema = ContactForm()
    try:
        valid_data = schema.load(data)
    except ValidationError as err:
        response_data.update({
            'message': 'Invalid input data',
            'errors': err.messages
        })
        return jsonify(response_data), 400

    name = valid_data.get('name')
    email = valid_data.get('email')
    phone_number = valid_data.get('phone_number')
    message = valid_data.get('message')

    user_contact =  Contact_details(name=name, email=email, phone_number=phone_number,message=message )
    contact_id = user_contact.save()
    contact_data = schema.dump(user_contact)
    print("contect-data>>>>",contact_data)

    response = make_response(
        jsonify({
            'success': True,
            'message': 'Contact form submitted successfully ',
            'admin': str(contact_data),
            "user_id":str(contact_id)
        })
    ), 200
    return response
@contact_bp.route('/update_leads/<string:contact_id>', methods=['PUT'])
def update_leads(contact_id):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    # Filter out any fields not defined in the schema
    try:
        # Load and validate the input data
        validated_data = ContactForm(partial=True).load(data)
    except ValidationError as err:
        return jsonify({"message": err.messages, "success": False}), 400

    try:
        result = contact_form.update_one({'_id': ObjectId(contact_id)}, {'$set': validated_data})
        if result.matched_count > 0:
            updated_product = contact_form.find_one({'_id': ObjectId(contact_id)})
            updated_product['_id'] = str(updated_product['_id'])
            return jsonify({"validated_data": updated_product, "success": True}), 200
        else:
            return jsonify({'message': 'Product not found', "success": False}), 404
    except Exception as e:
        return jsonify({'message': str(e), "success": False}), 400

@contact_bp.route("/get_all_leads", methods=["GET"])
def get_all():
    all_leads = list(contact_form.find([]))

    # Convert BSON to Python data types
    leads_list = []

    for lead in all_leads:
        # Convert ObjectId to string for serialization
        lead['_id'] = str(lead['_id'])
        leads_list.append(lead)

    total_leads = len(leads_list)

    response_data = {
        'total_leads': total_leads,
        'leads_list': leads_list,
    }
    return jsonify(response_data)


@contact_bp.route("/get_lead/<lead_id>", methods=["GET"])
def get_lead(lead_id):
    try:
        # Fetch the lead from the database using the provided lead_id
        lead = contact_form.find_one({"_id": ObjectId(lead_id)})

        if lead is None:
            return jsonify({"error": "Lead not found"}), 404

        # Convert ObjectId to string for JSON serialization
        lead['_id'] = str(lead['_id'])

        # Return the lead data in the response
        return jsonify(lead)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
