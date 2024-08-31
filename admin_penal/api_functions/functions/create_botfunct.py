from admin_penal.api_functions.models.createbot_models import insert_bot
from bson import ObjectId
from functools import wraps
from flask import request, jsonify, Blueprint
import jwt
from bson import ObjectId
from admin_penal.db_config import sub_admins

createchat_bp= Blueprint('create_chat', __name__)

def is_createchat(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Authorization header missing'}), 401

        token = auth_header.split(' ')[1]
        print("token>>>>>>>>>>>>", token) # Extract token from header
        try:
            payload = jwt.decode(token, 'NGi7Yovl6k1GZ1ZL90UCg4jaxE9RrkVr', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        user_id = payload.get('user_id')

        if not user_id:
            return jsonify({'error': 'Invalid token'}), 401

        try:
            user_id = ObjectId(user_id)
        except Exception as e:
            return jsonify({'error': 'Invalid user ID format'}), 401

        user = sub_admins.find_one({'_id': user_id})
        print("user>>>>>>>>>>>", user)

        if not user:
            return jsonify({'error': 'User not found'}), 401

        # Pass user data to the decorated function
        return func(user, *args, **kwargs)

    return decorated_function

def create_botfunt(data, user):
    chatbot_name = data.get("chatbot_name")
    chatbot_type = data.get("chatbot_type")
    chatbot_description = data.get("chatbot_description")
    created_by = ObjectId(user['_id'])  # Get the user ID from the user object

    chatbot_data = {
        'name': chatbot_name,
        'type': chatbot_type,
        'description': chatbot_description,
        'created_by': created_by  # Add user ID to the chatbot data
    }

    print("chatbot data", chatbot_data)
    insert_data = insert_bot(chatbot_data)
    print("insert data", insert_data)
    return insert_data


