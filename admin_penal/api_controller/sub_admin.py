from flask import Blueprint, request, jsonify,make_response,Flask
from marshmallow import ValidationError
from admin_penal.api_functions.models.sub_adminmodel  import User
from admin_penal.api_functions.schemas.sub_adminschema import UserSchema,UpdateSchema
from admin_penal.api_functions.functions.sub_adminfunct import password_conditions,generate_token,is_subadmin,generate_otp,send_otp_email,check_role,generate_reset_token,send_activation_email
# from admin_penal.api_functions.functions.admin_func import is_authenticated
from werkzeug.security import generate_password_hash, check_password_hash
from admin_penal.db_config import sub_admins
from datetime import datetime, timedelta
from bson import ObjectId
from flask import jsonify
from flask_cors import CORS
from admin_penal.api_functions.functions.sub_adminfunct import generate_access_token
import jwt


user_bp = Blueprint('user_bp', __name__)
CORS(user_bp)
# app.config['SECRET_KEY'] = 'your_secret_key'

# client = MongoClient('mongodb://localhost:27017/')
# db = client['admin_db']
# # super_admins = db['super_admins']
# sub_admins = db['sub_admins']

# Create a super admin (for setup purposes)

#user registration routes>>>>>>>>>>>>>>>>>>
@user_bp.route('/user/register', methods=['POST'])
def register():
    response_data = {
        'success': False,  # Default to False
        'message': 'An error occurred',  # Default message
    }
    data = request.get_json()
    schema = UserSchema()
    try:
        valid_data = schema.load(data)
    except ValidationError as err:
        # Extract a specific error message (for the first encountered error)
        first_error_message = next(iter(err.messages.values()), 'Invalid input data')

        response_data = {
            'success': False,
            'message': first_error_message[0]
        }
        return jsonify(response_data), 400

    username = valid_data.get('username')
    email = valid_data.get('email')
    phone_number = valid_data.get('phone_number')
    password= valid_data.get('password')
    role = valid_data.get('role')

    is_valid, status_code = password_conditions(password)

    if not is_valid:
        response_data.update({
            'message': 'Please use the correct password conditions'
        })
        return jsonify(response_data), status_code

    if User.find_by_email(email):
        response_data.update({
            'message': 'This email user already exists'
        })
        return jsonify(response_data), 400


    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, phone_number=phone_number, password=hashed_password,role=role)
    user_id = user.save()
    user_data = schema.dump(user)
    print("user-data>>>>",user_data )


    # return jsonify({'message': 'Registration successful! Welcome to logya soft tech.'}), 200
    response = make_response(
        jsonify({
            'success': True,
            'message': 'user registered successfully',
            'user': str(user_data),
            "user_id":str(user_id)
        })
    ), 200
    return response

#login and otp sending routes>>>>>>>>>>>>>>>>>
@user_bp.route('/user/login', methods=['POST'])
@check_role('user')
def login(user_lo):
    data = request.get_json()
    email = data.get('email')
    user_data = sub_admins.find_one({'email': email})
    print("user_data", user_data)

    if user_data and check_password_hash(user_data.get('password'), data.get('password')):
        # Get user details
        username = user_data.get('username')
        user_id = user_data.get('_id')

        # Generate token
        token = generate_token(user_id)

        # Set expiration time for the token
        token_expiration_time = datetime.utcnow() + timedelta(seconds=60)

        # Update user document with the token
        sub_admins.update_one({'_id': user_id}, {'$set': {'token': token}})

        # Generate OTP and expiration time
        otp, otp_expiration_time = generate_otp()

        # Update user document with the OTP and its expiration
        sub_admins.update_one(
            {'_id': user_id},
            {'$set': {'otp': otp, 'otp_expiration': otp_expiration_time}}
        )

        # Send OTP via email
        send_otp_email(email, otp)

        # Response with username, token, and OTP details
        response_data = {
            'message': f'Login successful, OTP sent to {email} successfully',
            'success': True
        }

        # Create response
        response = make_response(jsonify(response_data))
        print("response>>>>>>>>>>>>", response)

        # Set cookie with the token
        response.set_cookie('token', token, httponly=True, expires=token_expiration_time)

        return response
    else:
        return jsonify({
            'message': 'Given password or email does not match',
            'success': False,
            'status':401
        }), 401
#verify otp routs>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@user_bp.route('/user/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = str(data.get('otp'))  # Convert OTP to string for consistent comparison
    print("Received OTP:", otp)

    # Find user by email
    user_data = sub_admins.find_one({'email': email})
    if not user_data:
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404

    # Check if OTP matches and is not expired
    stored_otp = str(user_data.get('otp'))  # Ensure stored OTP is also a string
    print("Stored OTP:", stored_otp)
    otp_expiration_time = user_data.get('otp_expiration')

    # Log for debugging
    print(f"Received OTP: {otp}, Stored OTP: {stored_otp}, Expiration Time: {otp_expiration_time}, Current Time: {datetime.utcnow()}")

    if stored_otp != otp:
        return jsonify({
            'success': False,
            'message': 'Invalid OTP'
        }), 401

    if datetime.utcnow() > otp_expiration_time:
        return jsonify({
            'success': False,
            'message': 'OTP has expired'
        }), 401

    # OTP is valid, return login success message with user details and token
    response_data = {
        'message': 'Login successful. OTP has been verified.',
        'token': user_data.get('token'),
        'username': user_data.get('username'),
        'email': email,
        'user_id': str(user_data.get('_id')),
        'success': True
    }

    return jsonify(response_data), 200



#user profile >>>>>>>>>>>>>>>>>>>>>>>>>>>
@user_bp.route('/user/profile',methods=['GET'])
@is_subadmin('user')
def protected_route(user):
    # Add the 'user' parameter
    # Your protected route logic here
    user_info = {
        'username': user.get('username'),
        'email': user.get('email'),
        'phone_number': user.get('phone_number'),

    }
    return jsonify({'message': 'Welcome, authenticated super user!', 'user_info': user_info,'success':True})


@user_bp.route('/user/refresh-token', methods=['POST'])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get('refreshToken')

    try:
        # Decode the refresh token
        decoded = jwt.decode(refresh_token, 'NGi7Yovl6k1GZ1ZL90UCg4jaxE9RrkVr', algorithms=['HS256'])
        user_id = decoded['user_id']

        # Verify if refresh token matches the one stored in DB
        user_data = sub_admins.find_one({'_id': ObjectId(user_id)})
        print("user_data>>>>>>>>>>>>>>",user_data)
        if user_data and user_data.get('token') == refresh_token:
            # Generate a new access token
            new_access_token = generate_access_token(user_id)
            print("new_access_token>>>>>>>>>>>>>>>>>>>>>>",new_access_token)
            data = sub_admins.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {'token': new_access_token}}
            )
            print("data", data)
            return jsonify({
                'access_token': new_access_token,
                'message': 'Access token refreshed successfully',
                'success': True
            }), 200
        else:
            return jsonify({'message': 'Invalid refresh token', 'success': False}), 401

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token expired', 'success': False}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token', 'success': False}), 401


#resend otp routes>>>>>>>>>>>>>>>>>>>>
@user_bp.route('/user/resend-otp', methods=['POST'])
def resend_otp():
    data = request.get_json()
    email = data.get('email')
    print("email",email)

    user = sub_admins.find_one({'email': email})
    print("user",user)
    if not user:
        return jsonify({'message': 'User not found','success':False}), 404

    otp, expiration_time = generate_otp()
    print("otp,expiration_time",otp,expiration_time)
    data=sub_admins.update_one(
        {'email': email},
        {'$set': {'otp': otp, 'otp_expiration': expiration_time}}
    )
    print("data",data)

    send_otp_email(email, otp)

    return jsonify({'message': f'OTP sent {email} successfully','success':True}), 200

#forget password routes>>>>>>>>>>>>>>>
@user_bp.route('/user/forgot-password', methods=['POST'])
def request_reset():
    data = request.get_json()
    email = data.get('email')

    user = sub_admins.find_one({'email': email})

    if not user:
        return jsonify({'message': 'User not found','success':False}), 404

    reset_token = generate_reset_token()
    expiration_time = datetime.utcnow() + timedelta(hours=1)

    sub_admins.update_one(
        {'email': email},
        {'$set': {'reset_token': reset_token, 'reset_token_expiration': expiration_time}}
    )

    send_activation_email(email, reset_token)

    return jsonify({'message': 'Activation email sent successfully','success':True})

#reset password>>>>>>>>>>>>>>>
@user_bp.route('/user/reset-password/<reset_token>', methods=["POST"])
def reset(reset_token):
    data = request.get_json()
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    user = sub_admins.find_one({
        'reset_token': reset_token,
        'reset_token_expiration': {'$gt': datetime.utcnow()}
    })
    print("user>>>>>>>>>>>>>>",user)
    if not user:
        return jsonify({'message': 'Invalid reset token','success':False}), 400

    if data['new_password'] != data['confirm_password']:
        return jsonify({'message': 'Passwords do not match','success':False}), 400

    hashed_password = generate_password_hash(new_password)

    sub_admins.update_one(
        {'reset_token': reset_token},
        {'$set': {'password': hashed_password}, '$unset': {'reset_token': '', 'reset_token_expiration': ''}}
    )

    return jsonify({'message': 'Password reset successful','success':True})


#get all users routes>>>>>>>>>>>>>>>>>
@user_bp.route('/super_admin/user/getall_user', methods=['GET'])
def get_all():
    all_sub_admin = list(sub_admins.find({}))

    # Convert BSON to Python data types
    subadmin_list = []
    for user in all_sub_admin:
        # Convert ObjectId to string for serialization
        user['_id'] = str(user['_id'])

        # If 'super_admin_id' exists, convert it to a string
        if 'super_admin_id' in user:
            user['super_admin_id'] = str(user['super_admin_id'])

        # If 'otp_expiration' exists and is a datetime, convert it to a string
        if 'otp_expiration' in user and isinstance(user['otp_expiration'], datetime):
            user['otp_expiration'] = user['otp_expiration'].isoformat()

        subadmin_list.append(user)

    total_sub_admins = len(subadmin_list)

    response_data = {
        'total_users': total_sub_admins,
        'user_list': subadmin_list,
        'success':True
    }

    return jsonify(response_data), 200


#delete users>>>>>>>>>>>>>>>>>>>>
@user_bp.route('/super_admin/user/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Convert user_id to ObjectId
        user_id = ObjectId(user_id)

        # Find and delete the user
        result = sub_admins.delete_one({'_id': user_id})

        if result.deleted_count == 1:
            response_data = {
                'message': 'User deleted successfully',
                'success': True
            }
            return jsonify(response_data), 200
        else:
            return jsonify({
                'message': 'User not found',
                'success': False
            }), 404
    except Exception as e:
        return jsonify({
            'message': f'An error occurred: {str(e)}',
            'success': False
        }), 500


@user_bp.route('/super_admin/user/update/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    schema = UpdateSchema(partial=True)  # Allow partial updates

    try:
        valid_data = schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({'message': 'Invalid input data', 'errors': err.messages, 'success': False,'status':400}), 400

    # Update user in the database
    # Assuming you have a method to find and update user
    result = sub_admins.update_one({'_id': ObjectId(user_id)}, {'$set': valid_data})

    if result.matched_count:
        return jsonify({'message': 'User updated successfully', 'success': True,'status':200}), 200
    else:
        return jsonify({'message': 'User not found', 'success': False,'status':404}), 404

