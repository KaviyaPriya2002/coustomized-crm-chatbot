# from flask import Flask, request, jsonify
# from flask_pymongo import PyMongo
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# import datetime
# from bson.objectid import ObjectId
#
# app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/chatbotdb"
# app.config["JWT_SECRET_KEY"] = "your_secret_key"
#
# mongo = PyMongo(app)
# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)
#
#
# # Routes
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     username = data['username']
#     email = data['email']
#     password = data['password']
#     password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
#
#     mongo.db.users.insert_one({
#         "username": username,
#         "email": email,
#         "password_hash": password_hash,
#         "created_at": datetime.datetime.utcnow()
#     })
#
#     return jsonify({"msg": "User registered successfully"}), 201
#
#
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data['email']
#     password = data['password']
#     user = mongo.db.users.find_one({"email": email})
#
#     if user and bcrypt.check_password_hash(user['password_hash'], password):
#         access_token = create_access_token(identity=str(user['_id']))
#         return jsonify({"access_token": access_token}), 200
#     else:
#         return jsonify({"msg": "Invalid credentials"}), 401
#
#
# @app.route('/chatbots', methods=['GET', 'POST'])
# @jwt_required()
# def manage_chatbots():
#     if request.method == 'POST':
#         data = request.get_json()
#         user_id = get_jwt_identity()
#         chatbot_data = {
#             "user_id": ObjectId(user_id),
#             "name": data['name'],
#             "nodes": data['nodes'],
#             "created_at": datetime.datetime.utcnow()
#         }
#         mongo.db.chatbots.insert_one(chatbot_data)
#         return jsonify({"msg": "Chatbot created successfully"}), 201
#
#     user_id = get_jwt_identity()
#     chatbots = list(mongo.db.chatbots.find({"user_id": ObjectId(user_id)}))
#     return jsonify(chatbots), 200
#
#
# @app.route('/interact', methods=['POST'])
# def interact():
#     data = request.get_json()
#     chatbot_id = data['chatbot_id']
#     user_input = data['user_input']
#
#     chatbot = mongo.db.chatbots.find_one({"_id": ObjectId(chatbot_id)})
#     nodes = chatbot['nodes']
#
#     response_text = ""
#     response_image_url = ""
#
#     # Iterate through nodes to generate the response
#     for node in nodes:
#         if node['type'] == 'input':
#             last_utterance = user_input
#         elif node['type'] == 'ai_response':
#             response_text = node['content']['text'].format(last_utterance=last_utterance)
#             response_image_url = node['content'].get('image_url', "")
#
#     # Store interaction
#     interaction_data = {
#         "user_id": chatbot['user_id'],
#         "chatbot_id": chatbot_id,
#         "session_id": "unique_session_id",  # Generate a unique session ID
#         "interaction": [
#             {
#                 "timestamp": datetime.datetime.utcnow(),
#                 "user_input": user_input,
#                 "bot_response": {
#                     "text": response_text,
#                     "image_url": response_image_url
#                 }
#             }
#         ]
#     }
#     mongo.db.interactions.insert_one(interaction_data)
#
#     return jsonify({"response": {"text": response_text, "image_url": response_image_url}}), 200
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)



