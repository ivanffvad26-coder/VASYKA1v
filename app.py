print("=== ЭТО МОЙ APP.PY ===")

from flask import Flask, render_template, request, redirect, url_for, session
from auth import auth
from json import json
from db import init_db

app = Flask(__name__)
app.secret_key = "secret-key"

app.register_blueprint(auth)

init_db()

@app.route("/")
def home():
    return "Messenger backend is running"


if __name__ == "__main__":
    app.run()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")
MESSAGES_FILE = os.path.join(BASE_DIR, "messages.json")

app = Flask(__name__)
app.secret_key = "super_secret_key"

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html")
        
        if not os.path.exists(USERS_FILE):
            return "Нет пользователей"
        
        with open(USERS_FILE, "r") as f:
            users = json.load(f)

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/chat")
        else:
            return "Неверный логин или пароль"
        
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, "w") as f:
                json.dump({}, f)

        with open(USERS_FILE, "r") as f:
            users = json.load(f)

        if username in users:
            return "Пользователь уже существует"
        
        users[username] = password

        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

        return redirect("/login")
    return render_template("register.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect("/login")
    #Загружаем сообщения
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
            messages = json.load(f)
    else:
        messages = []

    # если отправили сообщение
    if request.method == "POST":
        text =  request.form.get("text")

        if text:
            messages.append({
                "user": session["user"],
                "text": text
            })

            with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)

        return redirect("/chat")
    
    return render_template("chat.html", messages=messages)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )