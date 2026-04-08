import smtplib
import os
import gspread
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

app = Flask(__name__)

GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')

def log_to_sheets(name, email):
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append_row([name, email, timestamp])

def send_email(name, email):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER
    msg['Subject'] = f"New UrbanLine Waitlist Signup — {name}"
    body = f"""
New waitlist signup:

Name: {name}
Email: {email}
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
    send_email(name, email)
    log_to_sheets(name, email)
    return "You are on the list! We will be in touch when we launch."

if __name__ == '__main__':
    app.run(debug=True)
