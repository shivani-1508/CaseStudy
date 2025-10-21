from flask import Flask, render_template, request

app = Flask(__name__)

def check_strength(password):
    strength = 0

    if len(password) >= 8:
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.islower() for c in password):
        strength += 1
    if any(c in "!@#$%^&*()-_=+[]{};:'\",.<>?/|" for c in password):
        strength += 1

    if strength <= 2:
        return "Weak"
    elif strength == 3 or strength == 4:
        return "Medium"
    else:
        return "Strong"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    password = request.form['password']
    result = check_strength(password)
    return render_template('result.html', password=password, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port="5000",debug=True)
