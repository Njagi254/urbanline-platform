import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

def send_email(name, email, phone, date, duration, message):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER
    msg['Subject'] = f"New UrbanLine Booking Request from {name}"

    body = f"""
New booking request received:

Name: {name}
Email: {email}
Phone: {phone}
Date: {date}
Duration: {duration}
Message: {message}
    """

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    date = request.form['date']
    duration = request.form['duration']
    message = request.form.get('message', '')

    send_email(name, email, phone, date, duration, message)

    return "Thanks for your request! We will be in touch shortly."

if __name__ == '__main__':
    app.run(debug=True)
