
from flask import Flask,Blueprint,request,jsonify
import jwt
from datetime import timedelta,datetime
from admin_penal.db_config import sub_admins
from bson import ObjectId
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask_mail import Mail,Message
import string
import random
from werkzeug.security import  check_password_hash

mail = Mail()

# Initialize Flask-Mail with the Flask app
def password_conditions(password):
    if len(password) < 8:
        return False, 400
    if not any(char.islower() for char in password):
        return False, 400
    if not any(char.isupper() for char in password):
        return False, 400
    if not any(char.isdigit() for char in password):
        return False, 400
    if not any(char in '@$!%*?&' for char in password):
        return False, 400
    return True, 200

def generate_token(user_id):
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({'user_id': str(user_id), 'exp': expiration_time}, 'NGi7Yovl6k1GZ1ZL90UCg4jaxE9RrkVr',
                       algorithm='HS256')
    return token

def is_subadmin(required_role):
    def decorator(func):

        @wraps(func)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({'error': 'Authorization header missing'}), 401

            token = auth_header.split(' ')[1]
            print(token)# Extract token from header
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
            print("user>>>>>",user)
            print(user)


            if not user:
                return jsonify({'error': 'User not found'}), 401


            user_role = user.get('role')
            print("user-role",user_role)
            if user_role != required_role:
                return jsonify({'error': 'Access denied: Unauthorized role'}), 403

            # Pass user data to the decorated function
            return func(user, *args, **kwargs)

        return decorated_function

    return decorator
def check_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Extract email and password from the request
            data = request.json
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return jsonify({'error': 'Email and password are required','success':False}), 400

            # Lookup user in MongoDB
            user = sub_admins.find_one({'email': email})
            if user is None or not check_password_hash(user['password'], password):
                return jsonify({'error': 'Invalid credentials','success':False}), 401

            user_role = user.get('role')
            print("user-role:", user_role)

            if user_role != required_role:
                return jsonify({'error': 'Access denied: Unauthorized role','success':False}), 403

            # Pass user data to the decorated function
            return f(user, *args, **kwargs)

        return decorated_function
    return decorator
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False
    return email

def send_otp_email(email, otp):
    msg = Message('Your OTP Code', sender='kaviyapriyavenkat2002@gmail.com', recipients=[email])
    msg.body = f'Your OTP code is {otp}. It is valid for 1 minutes.'
    mail.send(msg)


def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    expiration_time = datetime.utcnow() + timedelta(minutes=5)
    print("expiration_time||||||||||||||||||||||||||||||",expiration_time)
    return otp, expiration_time

def generate_reset_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
def send_activation_email(email, reset_token):
    # mail = current_app.extensions['mail']
    reset_link = f'http://192.168.1.12:5789/user/resetPassword/{reset_token}'
    msg = Message('Reset Your Password', sender='sayathra123@gmail.com', recipients=[email])
    msg.body = f'Click the following link to reset your password: {reset_link}'
    mail.send(msg)