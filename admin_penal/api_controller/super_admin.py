# api_controller/user_routes.py
from flask import Blueprint, request, jsonify,make_response
from marshmallow import ValidationError
from admin_penal.api_functions.models.admin_models import super_admin
from admin_penal.api_functions.schemas.admin_schemas import Superadmin_Schema
from admin_penal.api_functions.functions.admin_func import password_conditions,generate_token,is_authenticated,generate_reset_token,send_activation_email,generate_otp,send_otp_email,check_role
from werkzeug.security import generate_password_hash, check_password_hash
from admin_penal.db_config import collection,sub_admins
from datetime import datetime, timedelta
from flask_cors import CORS

admin_bp = Blueprint('super_admin', __name__)
CORS(admin_bp)

# @admin_bp.before_request
# def block_options_requests():
#     if request.method == 'OPTIONS':
#         return jsonify({'message': 'Method Not Allowed'}), 405

@admin_bp.route('/super_admin/register', methods=['POST'])
def register():
    response_data = {
        'success': False,  # Default to False
        'message': 'An error occurred',  # Default message
    }
    data = request.get_json()
    schema = Superadmin_Schema()
    try:
        valid_data = schema.load(data)
    except ValidationError as err:
        response_data.update({
            'message': 'Invalid input data',
            'errors': err.messages
        })
        return jsonify(response_data), 400

    adminname = valid_data.get('adminname')
    email = valid_data.get('email')
    phone_number = valid_data.get('phone_number')
    password = valid_data.get('password')
    role = valid_data.get('role')

    is_valid, status_code = password_conditions(password)

    if not is_valid:
        response_data.update({
            'message': 'Please use the correct password conditions'
        })
        return jsonify(response_data), status_code

    if super_admin.find_by_email(email):
        response_data.update({
            'message': 'This email admin already exists'
        })
        return jsonify(response_data), 400


    hashed_password = generate_password_hash(password)
    admin = super_admin(adminname=adminname, email=email, phone_number=phone_number, password=hashed_password,role=role)
    admin_id = admin.save()
    admin_data = schema.dump(admin)
    print("admin-data>>>>",admin_data)


    # return jsonify({'message': 'Registration successful! Welcome to logya soft tech.'}), 200
    response = make_response(
        jsonify({
            'success': True,
            'message': 'Admin registered successfully',
            'admin': str(admin_data),
            "user_id":str(admin_id)
        })
    ), 200
    return response
@admin_bp.route('/super_admin/login', methods=['POST'])
@check_role('super-admin')
def login(user):
    data = request.get_json()
    admin_data = collection.find_one({'email': data.get('email')})
    print("admindata",admin_data)


    if admin_data and check_password_hash(admin_data.get('password'), data.get('password')):
        # Get user details
        adminname = admin_data.get('adminname')
        email = admin_data.get('email')
        admin_id = admin_data.get('_id')

        # Generate token
        token = generate_token(admin_id)

        # Set expiration time for the token
        expiration_time = datetime.utcnow() + timedelta(seconds=6)

        # Update user document with the token
        collection.update_one({'_id': admin_id}, {'$set': {'token': token}})

        # Response with username and token
        response_data = {
            'message': 'Login successful',
            'token': token,
            'adminname': adminname,
            'email': email,
            'admin_id':str(admin_id),
            'success':True
        }

        # Create response
        response = make_response(jsonify(response_data))
        print("response>>>>>>>>>>>>",response)

        # Set cookie with the token
        response.set_cookie('token', token, httponly=True, expires=expiration_time)

        return response
    else:
        return jsonify({
            'message': 'Given password or email does not match',
            'success': False
        }), 401

# @admin_bp.route('/super_admin/login', methods=['POST'])
# @check_role('super-admin')
# def login(user):
#     data = request.get_json()
#     email = data.get('email')
#     admin_data = collection.find_one({'email': email})
#     print("admindata", admin_data)
#
#     if admin_data and check_password_hash(admin_data.get('password'), data.get('password')):
#         # Get user details
#         adminname = admin_data.get('adminname')
#         admin_id = admin_data.get('_id')
#
#         # Generate token
#         token = generate_token(admin_id)
#
#         # Set expiration time for the token
#         token_expiration_time = datetime.utcnow() + timedelta(seconds=6)
#
#         # Update user document with the token
#         collection.update_one({'_id': admin_id}, {'$set': {'token': token}})
#
#         # Generate OTP and expiration time
#         otp, otp_expiration_time = generate_otp()
#
#         # Update user document with the OTP and its expiration
#         collection.update_one(
#             {'_id': admin_id},
#             {'$set': {'otp': otp, 'otp_expiration': otp_expiration_time}}
#         )
#
#         # Send OTP via email
#         send_otp_email(email, otp)
#
#         # Response with username, token, and OTP details
#         response_data = {
#             'message': f'Login successful,{email} OTP sent successfully',
#             # 'token': token,
#             # 'adminname': adminname,
#             # 'email': email,
#             # 'admin_id': str(admin_id),
#             # 'otp': otp,
#             # 'otp_expiration': otp_expiration_time,
#             'success': True
#         }
#
#         # Create response
#         response = make_response(jsonify(response_data))
#         print("response>>>>>>>>>>>>", response)
#
#         # Set cookie with the token
#         response.set_cookie('token', token, httponly=True, expires=token_expiration_time)
#
#         return response
#     else:
#         return jsonify({
#             'message': 'Given password or email does not match',
#             'success': False
#         }), 401
@admin_bp.route('/super_admin/profile')
@is_authenticated('super-admin')
def protected_route(user):
    # Add the 'user' parameter
    # Your protected route logic here
    admin_info = {
        'adminname': user.get('adminname'),
        'email': user.get('email'),
        'phone_number': user.get('phone_number'),

    }
    return jsonify({'message': 'Welcome, authenticated super admin!', 'user_info': admin_info,'success':True})

@admin_bp.route('/super_admin/forgot-password', methods=['POST'])
def request_reset():
    data = request.get_json()
    email = data.get('email')

    user = collection.find_one({'email': email})

    if not user:
        return jsonify({'message': 'User not found','success':False}), 404

    reset_token = generate_reset_token()
    expiration_time = datetime.utcnow() + timedelta(hours=1)

    collection.update_one(
        {'email': email},
        {'$set': {'reset_token': reset_token, 'reset_token_expiration': expiration_time}}
    )

    send_activation_email(email, reset_token)

    return jsonify({'message': 'Activation email sent successfully','success':True})

@admin_bp.route('/super_admin/resend-otp', methods=['POST'])
def resend_otp():
    data = request.get_json()
    email = data.get('email')
    print("email",email)

    user = collection.find_one({'email': email})
    print("user",user)
    if not user:
        return jsonify({'message': 'User not found','success':False}), 404

    otp, expiration_time = generate_otp()
    print("otp,expiration_time",otp,expiration_time)
    data=collection.update_one(
        {'email': email},
        {'$set': {'otp': otp, 'otp_expiration': expiration_time}}
    )
    print("data",data)

    send_otp_email(email, otp)

    return jsonify({'message': f'OTP sent {email} successfully','success':True}), 200
@admin_bp.route('/super_admin/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = str(data.get('otp'))  # Convert OTP to string for consistent comparison
    print("Received OTP:", otp)

    # Find user by email
    admin_data = collection.find_one({'email': email})
    if not admin_data:
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404

    # Check if OTP matches and is not expired
    stored_otp = str(admin_data.get('otp'))  # Ensure stored OTP is also a string
    print("Stored OTP:", stored_otp)
    otp_expiration_time = admin_data.get('otp_expiration')

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
        'token': admin_data.get('token'),
        'adminname': admin_data.get('adminname'),
        'email': email,
        'admin_id': str(admin_data.get('_id')),
        'success': True
    }

    return jsonify(response_data), 200


# @admin_bp.route('/super_admin/verify-otp', methods=['POST'])
# def verify_otp():
#     data = request.get_json()
#     email = data.get('email')
#     otp = data.get('otp')
#
#     # Debugging: Print the received OTP and email
#     print(f"Received OTP: {otp}, Email: {email}")
#
#     # Find user in the database
#     user = collection.find_one({'email': email})
#     print(f"User found: {user}")
#
#     if not user:
#         return jsonify({'success': False, 'message': 'User not found'}), 404
#
#     stored_otp = user.get('otp')
#     otp_expiration = user.get('otp_expiration')
#
#     # Debugging: Print stored OTP and expiration
#     print(f"Stored OTP: {stored_otp}, OTP Expiration: {otp_expiration}")
#
#     if not stored_otp or not otp_expiration:
#         return jsonify({'success': False, 'message': 'OTP not found or expired'}), 400
#
#     if datetime.utcnow() > otp_expiration:
#         return jsonify({'success': False, 'message': 'OTP has expired'}), 400
#
#     if str(stored_otp) != str(otp):
#         return jsonify({'success': False, 'message': 'Invalid OTP'}), 400
#
#     # OTP is valid, you can now mark the user as verified or perform other actions
#     collection.update_one({'email': email}, {'$unset': {'otp': "", 'otp_expiration': ""}})
#
#     return jsonify({'success': True, 'message': 'OTP verified successfully'}), 200

@admin_bp.route('/super_admin/resetPassword/<reset_token>', methods=["POST"])
def reset(reset_token):
    data = request.get_json()
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    admin = collection.find_one({
        'reset_token': reset_token,
        'reset_token_expiration': {'$gt': datetime.utcnow()}
    })

    if not admin:
        return jsonify({'message': 'Invalid reset token','success':False}), 400

    if data['new_password'] != data['confirm_password']:
        return jsonify({'message': 'Passwords do not match','success':False}), 400

    hashed_password = generate_password_hash(new_password)

    collection.update_one(
        {'reset_token': reset_token},
        {'$set': {'password': hashed_password}, '$unset': {'reset_token': '', 'reset_token_expiration': ''}}
    )

    return jsonify({'message': 'Password reset successful','success':True})

