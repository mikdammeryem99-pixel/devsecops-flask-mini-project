from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)
SECRET_KEY = "hardcoded-secret-key"  # ❌ vuln volontaire

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ping", methods=["POST"])
def ping():
    host = request.form.get("host")
    cmd = f"ping -c 1 {host}"  # ❌ command injection
    output = subprocess.check_output(cmd, shell=True)
    return output.decode()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
