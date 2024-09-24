from django.template.defaultfilters import title
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from admin_penal.api_functions.schemas.plan_schema import ManagePlanSchema
from admin_penal.api_functions.functions.plan_function import SubscriptionService
from admin_penal.api_functions.models.plan_models import SubscriptionPlan
from admin_penal.db_config import manage_plan

plan_bp = Blueprint('plans', __name__)
  # Assuming `db` is your MongoDB instance

@plan_bp.route('/create-plan', methods=['POST'])
def create_plan():
    try:
        data = request.get_json()
        print(data)

        # Validate input using Marshmallow schema
        plan_schema = ManagePlanSchema()
        plan_data = plan_schema.load(data)
        print(plan_data)

        # Create plan and save it in the database
        manage_plan_service = SubscriptionPlan()
        print("manage_plan_service>>>>", manage_plan_service)

        # Call the method to create a new plan
        manage_plan_id = manage_plan_service.create_plan(plan_data)

        # Respond with the created plan's ID
        return jsonify({
            "message": "Plan created successfully",
            "plan_id": manage_plan_id,
            "success": True,
            "status code": 200,
            "plan data": plan_data  # plan_data is already validated
        }), 200

    except ValidationError as err:
        # Catch validation errors and respond accordingly
        return jsonify({
            "success": False,
            "message": err.messages  # Use your preferred error format
        }), 400


@plan_bp.route('/get-all-plans', methods=['GET'])
# @is_authenticated('super-admin')  # Uncomment if authentication is needed
def get_all_plans():
    plan_service = SubscriptionPlan()
    all_plans = plan_service.get_all_plans()
    return jsonify({"plans": all_plans, "success": True, "status code": 200}), 200

@plan_bp.route('/delete-plan/<plan_id>', methods=['DELETE'])
def delete_faq(plan_id):
    manage_plan_service = SubscriptionPlan()
    deleted_count = manage_plan_service.delete_plan(plan_id)

    if deleted_count > 0:
        return jsonify({"message": "manage plan deleted successfully", "success": True, "status code": 200}), 200
    else:
        return jsonify({"message": "manage plan  not found", "success": False, "status code": 404}), 404




