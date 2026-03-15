from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

choices = ["rock", "paper", "scissors"]

def determine_winner(user, computer):

    if user == computer:
        return "Tie"

    if (user == "rock" and computer == "scissors") or \
       (user == "scissors" and computer == "paper") or \
       (user == "paper" and computer == "rock"):
        return "You Win!"

    return "Computer Wins!"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/play", methods=["POST"])
def play():

    user_choice = request.json["choice"]
    computer_choice = random.choice(choices)

    result = determine_winner(user_choice, computer_choice)

    return jsonify({
        "user": user_choice,
        "computer": computer_choice,
        "result": result
    })


if __name__ == "__main__":
    app.run(debug=True)