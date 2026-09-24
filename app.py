# app.py

from flask import Flask, render_template, request, session
from model import questions
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "f4a9c2e7d81b6") # Demo key only.


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/start")
def start():
    session["correct"] = 0
    session["incorrect"] = 0
    return render_template("question.html", question=questions[0][0], number=0)


@app.route("/answer", methods=["POST"])
def answer():
    number = int(request.form["number"])
    user_answer = request.form["answer"]

    question, correct_answer = questions[number]

    if user_answer.lower() == correct_answer.lower():
        session["correct"] += 1
        result = "Correct!"
    else:
        session["incorrect"] += 1
        result = f"Incorrect. The answer was {correct_answer}."

    return render_template("result.html", result=result, number=number)


@app.route("/next", methods=["POST"])
def next_question():
    number = int(request.form["number"]) + 1

    if number >= len(questions):
        return render_template("finished.html", result="Quiz completed!", correct=session["correct"], incorrect=session["incorrect"])

    return render_template("question.html", question=questions[number][0], number=number)


if __name__ == "__main__":
    app.run(debug=True)