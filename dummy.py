# from functools import wraps
# import jwt
# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# from bson import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash
# import datetime
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'
#
# client = MongoClient('mongodb://localhost:27017/')
# db = client['admin_db']
# super_admins = db['super_admins']
# sub_admins = db['sub_admins']
#
# # Create a super admin (for setup purposes)
# @app.route('/create_super_admin', methods=['POST'])
# def create_super_admin():
#     data = request.get_json()
#     hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
#     super_admins.insert_one({
#         'username': data['username'],
#         'password': hashed_password
#     })
#     return jsonify({'message': 'Super admin created successfully'})
#
# # Super admin login
# @app.route('/login_super_admin', methods=['POST'])
# def login_super_admin():
#     data = request.get_json()
#     user = super_admins.find_one({'username': data['username']})
#     if user and check_password_hash(user['password'], data['password']):
#         token = jwt.encode({
#             'super_admin_id': str(user['_id']),
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#         }, app.config['SECRET_KEY'], algorithm='HS256')
#         return jsonify({'token': token})
#     return jsonify({'message': 'Invalid credentials'}), 401
#
# # Function to verify super admin token
# def token_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return jsonify({'error': 'Authorization header missing'}), 401
#
#         token = auth_header.split(' ')[1]
#         try:
#             payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             return jsonify({'error': 'Token has expired'}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({'error': 'Invalid token'}), 401
#
#         user_id = payload.get('super_admin_id')
#
#         if not user_id:
#             return jsonify({'error': 'Invalid token'}), 401
#
#         try:
#             user_id = ObjectId(user_id)
#         except Exception as e:
#             return jsonify({'error': 'Invalid user ID format'}), 401
#
#         current_super_admin = super_admins.find_one({'_id': user_id})
#
#         if not current_super_admin:
#             return jsonify({'error': 'User not found'}), 401
#
#         return f(current_super_admin, *args, **kwargs)
#
#     return decorated_function
#
# # Create a sub admin
# @app.route('/create_sub_admin', methods=['POST'])
# @token_required
# def create_sub_admin(current_super_admin):
#     data = request.get_json()
#     hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
#     sub_admins.insert_one({
#         'super_admin_id': current_super_admin['_id'],
#         'username': data['username'],
#         'password': hashed_password
#     })
#     return jsonify({'message': 'Sub admin created successfully'})
#
# # Get sub admins created by super admin
# @app.route('/get_sub_admins', methods=['GET'])
# @token_required
# def get_sub_admins(current_super_admin):
#     sub_admin_list = list(sub_admins.find({'super_admin_id': current_super_admin['_id']}))
#     for sub_admin in sub_admin_list:
#         sub_admin['_id'] = str(sub_admin['_id'])
#         sub_admin['super_admin_id'] = str(sub_admin['super_admin_id'])
#     return jsonify(sub_admin_list)
#
# if __name__ == '__main__':
#     app.run(debug=True, port=7890)
#
n=0
while(n<5):
    print('kaviya')
    n+=5