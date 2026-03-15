from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    length    = int(data.get("length", 16))
    use_upper = data.get("upper", True)
    use_lower = data.get("lower", True)
    use_nums  = data.get("nums",  True)
    use_syms  = data.get("syms",  True)

    if length < 6:
        return jsonify({"error": "Length must be at least 6"}), 400

    pool = ""
    required = []

    if use_upper:
        pool += string.ascii_uppercase
        required.append(random.choice(string.ascii_uppercase))

    if use_lower:
        pool += string.ascii_lowercase
        required.append(random.choice(string.ascii_lowercase))

    if use_nums:
        pool += string.digits
        required.append(random.choice(string.digits))

    if use_syms:
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        pool += symbols
        required.append(random.choice(symbols))

    if not pool:
        return jsonify({"error": "Select at least one character type"}), 400

    remaining = [random.choice(pool) for _ in range(length - len(required))]
    password_list = required + remaining
    random.shuffle(password_list)
    password = "".join(password_list)

    score = 0
    if length >= 8:  score += 1
    if length >= 12: score += 1
    if length >= 16: score += 1
    type_count = sum([use_upper, use_lower, use_nums, use_syms])
    if type_count >= 3: score += 1
    if type_count == 4 and length >= 12: score = min(score + 1, 4)
    score = min(score, 4)

    labels = ["", "Weak", "Fair", "Good", "Strong"]

    return jsonify({
        "password": password,
        "strength": score,
        "strength_label": labels[score]
    })

if __name__ == "__main__":
    app.run(debug=True)