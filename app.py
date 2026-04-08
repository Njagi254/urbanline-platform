from flask import Flask, render_template, request

app = Flask(__name__)

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

    print(f"New booking request from {name}")
    print(f"Email: {email} | Phone: {phone}")
    print(f"Date: {date} | Duration: {duration}")
    print(f"Message: {message}")

    return "Thanks for your request! We will be in touch shortly."

if __name__ == '__main__':
    app.run(debug=True)
