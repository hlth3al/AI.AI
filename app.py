import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GAPGPT_API_URL = "https://api.gapgpt.app/v1/chat/completions"
GAPGPT_API_KEY = "+LIVE_ACCESS_KEY"

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "active", "message": "AI.AI Backend is running"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True, silent=True) or {}
        messages = data.get("messages", [])
        if not messages:
            return jsonify({"error": "No messages"}), 400

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GAPGPT_API_KEY}"
        }
        payload = {
            "model": data.get("model", "gpt-4o-mini"),
            "messages": messages,
            "temperature": data.get("temperature", 0.7)
        }
        resp = requests.post(GAPGPT_API_URL, headers=headers, json=payload, timeout=60)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": "Server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
