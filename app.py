from flask import Flask
from auth import auth
from db import init_db
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "secret")

app.register_blueprint(auth)

init_db()

@app.route("/")
def home():
    return "OK"

if name == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))