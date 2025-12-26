from flask import Flask, request
import sqlite3
import bcrypt
import subprocess
import os

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password").encode()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    if result and bcrypt.checkpw(password, result[0]):
        return {"status": "success"}

    return {"status": "error"}, 401


@app.route("/ping", methods=["POST"])
def ping():
    host = request.json.get("host")

    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True
    )

    return {"output": result.stdout}


@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password").encode()
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return {"hash": hashed.decode()}


@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Secure DevSecOps API"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
