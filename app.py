from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import json, bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# تحميل بيانات المستخدمين
def load_users():
    with open("users.json") as f:
        return json.load(f)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    users = load_users()

    if username in users and bcrypt.checkpw(password.encode(), users[username].encode()):
        session["user"] = username
        return redirect(url_for("dashboard"))
    else:
        flash("Invalid username or password")
        return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
