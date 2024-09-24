from admin_penal.api_controller.super_admin import admin_bp
from admin_penal.api_controller.sub_admin import user_bp
from admin_penal.api_controller.faq_controller import faq_bp
# from admin_penal.api_controller.create_bot import createchat_bp
from admin_penal.api_controller.chatbot import chatbot_bp
from admin_penal.api_controller.contact_form import contact_bp
from admin_penal.api_controller.manage_plan import plan_bp
from user.api_controller.chatbot import bot_bp
from user.api_controller.chatbot_flow import flow_bp
from user.api_controller.intents import intent_bp
from flask import Flask
from flask_mail import Mail
import os
from dotenv import load_dotenv
from waitress import serve

load_dotenv()
# mode ='dev'

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

app.register_blueprint(admin_bp,url_prefix='/super_admin')
app.register_blueprint(user_bp)
app.register_blueprint(contact_bp,url_prefix='/super_admin')
app.register_blueprint(faq_bp,url_prefix='/super_admin')
app.register_blueprint(flow_bp,url_prefix='/user')
app.register_blueprint(plan_bp,url_prefix='/super_admin')
# app.register_blueprint(createchat_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(intent_bp)
app.register_blueprint(bot_bp,url_prefix='/user')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
