import os
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request, jsonify

EMAIL_ENV = "BOT_EMAIL"
PASSWORD_ENV = "BOT_PASSWORD"

EMAIL_FROM = "Email Bot"

# Nutrir-Com-Tempero env variable
RECIPIENT_ENV = "NUTRIR_RECIPIENT"

app = Flask(__name__)


# Email function logger endpoint
@app.route('/send', methods=['POST'])
def send_email():
    try:
        # Initialize session
        email = os.environ.get(EMAIL_ENV)
        password = os.environ.get(PASSWORD_ENV)

        session = authenticate_email(email, password)

        # Get data from request
        req_data = request.get_json()

        recipient = req_data['recipient']
        text = req_data['text']
        subject = req_data['subject']

        if is_subject_valid(subject) is False:
            return {'error': 'Invalid email body'}

        message = create_message(recipient, subject)
        message.attach(MIMEText(text, 'plain'))

        body = message.as_string()

        # Send the email
        session.sendmail(email, recipient, body)
        session.quit()

        return {'message': 'Email sent succesfully!'}

    except:
        return {'error': 'There was an error processing the request'}


def authenticate_email(email, password):
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(email, password)

    return session


def create_message(recipient, subject):
    message = MIMEMultipart()
    message['From'] = EMAIL_FROM
    message['To'] = recipient
    message['Subject'] = subject

    return message


def is_subject_valid(subject):
    # subject = ["Function", "'{function_name}'", "execution", "log"]
    subject_text = subject.split()

    valid_subject = [r"Function",
                     # <function name>
                     # [a-zA-Z_] = First char must be a letter or _
                     # [a-zA-Z_\d]* = The following chars can be either letters, numbers or _
                     r"'[a-zA-Z_][a-zA-Z_\d]*'",
                     r"execution",
                     r"log"]

    for text, pattern in zip(subject_text, valid_subject):
        match = re.match(pattern, text)

        if match is None:
            return False

    return True


# Nutrir-Com-Tempero contact form endpoint
@app.route('/contact', methods=['POST'])
def contact():
    try:
        recipient = os.environ.get(RECIPIENT_ENV)

        # Initialize session
        email = os.environ.get(EMAIL_ENV)
        password = os.environ.get(PASSWORD_ENV)

        session = authenticate_email(email, password)

        # Get data from request
        req_data = request.get_json()

        name = req_data['name']
        email_sender = req_data['email']

        # Validate email address
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_sender):
            return {'error': 'Invalid email address'}

        text = req_data['text']

        email_body = f"Remetente: {email_sender}\n\nMensagem: \n{text}\n"

        subject = f"Mensagem enviada por {name} em Nutrir Com Tempero"

        message = create_message(recipient, subject)
        message.attach(MIMEText(email_body, 'plain', 'utf-8'))

        body = message.as_string()

        # Send the email
        session.sendmail(email, recipient, body)
        session.quit()

        response = jsonify({'message': 'Email sent succesfully!'})
        response.headers.add("Access-Control-Allow-Origin", '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add("Access-Control-Allow-Headers",
                             'Origin,X-Requested-With,Content-Type,Accept,content-type,application/json')

        return response

    except:
        response = jsonify(
            {'error': 'There was an error processing the request'})
        response.headers.add("Access-Control-Allow-Origin", '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add("Access-Control-Allow-Headers",
                             'Origin,X-Requested-With,Content-Type,Accept,content-type,application/json')

        return response
