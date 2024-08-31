from flask import Flask
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Debug: Print loaded environment variables
print("MAIL_SERVER:", os.getenv('MAIL_SERVER'))
print("MAIL_PORT:", os.getenv('MAIL_PORT'))
print("MAIL_USE_TLS:", os.getenv('MAIL_USE_TLS'))
print("MAIL_USERNAME:", os.getenv('MAIL_USERNAME'))
print("MAIL_PASSWORD:", os.getenv('MAIL_PASSWORD'))

# Ensure the variables are loaded correctly
mail_server = os.getenv('MAIL_SERVER')
mail_port = os.getenv('MAIL_PORT')
mail_use_tls = os.getenv('MAIL_USE_TLS')
mail_username = os.getenv('MAIL_USERNAME')
mail_password = os.getenv('MAIL_PASSWORD')

if not all([mail_server, mail_port, mail_use_tls, mail_username, mail_password]):
    raise ValueError("One or more environment variables are missing.")

# Configure Flask-Mail using environment variables
app.config['MAIL_SERVER'] = mail_server
app.config['MAIL_PORT'] = int(mail_port)  # Ensure port is an integer
app.config['MAIL_USE_TLS'] = mail_use_tls == 'True'
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password

mail = Mail(app)

@app.route("/send-test-email",methods=['POST'])
def send_test_email():
    with app.app_context():
        msg = Message('Test Email', sender=app.config['MAIL_USERNAME'], recipients=['kaviyadharshini566@gmail.com'])
        msg.body = 'This is a test email.'
        try:
            mail.send(msg)
            return "Email sent successfully!"
        except Exception as e:
            return str(e)

if __name__ == "__main__":
    app.run(debug=True, port=5436, host='192.168.1.7')
