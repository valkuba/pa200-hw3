import os, json
import base64
from flask import Flask, render_template, request, redirect, url_for, flash
from azure.storage.queue import QueueClient

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
CONN_STR   = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
QUEUE_NAME = "newsletter-queue"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    email   = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    if not email or not message:
        flash("Vyplň email i zprávu.", "error")
        return redirect(url_for("index"))
    try:
        client = QueueClient.from_connection_string(CONN_STR, QUEUE_NAME)
        try:
            client.create_queue()
        except Exception:
            pass
        message = json.dumps({"email": email, "message": message})
        encoded = base64.b64encode(message.encode()).decode()
        client.send_message(encoded)
        flash(f"Zpráva pro {email} zařazena do fronty!", "success")
    except Exception as e:
        flash(f"Chyba: {e}", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
    