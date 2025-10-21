from flask import Flask, render_template, request

app = Flask(__name__)

def check_strength(password):
    """Return (score, label). Score 0..5"""
    score = 0

    if len(password) >= 8:
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c in "!@#$%^&*()-_=+[]{};:'\",.<>?/|\\`~" for c in password):
        score += 1

    if score <= 2:
        label = "Weak"
    elif score <= 4:
        label = "Medium"
    else:
        label = "Strong"

    return score, label

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    password = request.form.get('password', '')
    score, label = check_strength(password)
    # mask the password for display (show length only)
    masked = '•' * len(password) if password else ''
    suggestions = []
    if len(password) < 8:
        suggestions.append("Use at least 8 characters.")
    if not any(c.isdigit() for c in password):
        suggestions.append("Add numeric characters (0-9).")
    if not any(c.isupper() for c in password):
        suggestions.append("Add uppercase letters (A-Z).")
    if not any(c.islower() for c in password):
        suggestions.append("Add lowercase letters (a-z).")
    if not any(c in "!@#$%^&*()-_=+[]{};:'\",.<>?/|\\`~" for c in password):
        suggestions.append("Include special characters (e.g. !@#$%).")

    return render_template(
        'result.html',
        masked=masked,
        length=len(password),
        score=score,
        label=label,
        suggestions=suggestions
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
