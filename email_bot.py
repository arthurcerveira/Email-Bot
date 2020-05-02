import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request

app = Flask(__name__)

EMAIL_ENV = "BOT_EMAIL"
PASSWORD_ENV = "BOT_PASSWORD"


@app.route('/send', methods=['POST'])
def send_email():
    # Initialize session
    email = os.environ.get(EMAIL_ENV)
    password = os.environ.get(PASSWORD_ENV)

    session = authenticate_email(email, password)

    # Get data from request
    req_data = request.get_json()

    recipient = req_data['recipient']
    text = req_data['text']
    subject = req_data['subject']

    message = create_message(email, recipient, subject)
    message.attach(MIMEText(text, 'plain'))
    
    body = message.as_string()

    # Send the email
    session.sendmail(email, recipient, body)
    session.quit()

    return {'message': 'Email sent succesfully!'}


def authenticate_email(email, password):
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(email, password)

    return session


def create_message(email, recipient, subject):
    message = MIMEMultipart()
    message['From'] = email
    message['To'] = recipient
    message['Subject'] = subject

    return message