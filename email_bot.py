import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask

app = Flask(__name__)

@app.route('/')
def send_email():
    return 'Sending email...'