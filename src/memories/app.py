# app.py — Flask backend с AI и избранными

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json

app = Flask(__name__)
CORS(app)

FAVORITES_FILE = "favorites.json"
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Загрузка данных избранных (если файл есть)
def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)
    return {}

# Сохранение избранных
def save_favorites(data):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(data, f)

# Получить избранные для пользователя
@app.route("/favorites/<user>", methods=["GET"])
def get_favorites(user):
    data = load_favorites()
    return jsonify(data.get(user, []))

# Добавить в избранное
@app.route("/favorites/<user>", methods=["POST"])
def add_favorite(user):
    data = load_favorites()
    emoji = request.json.get("name")
    if not emoji:
        return jsonify({"error": "No emoji name provided"}), 400
    data.setdefault(user, [])
    if emoji not in data[user]:
        data[user].append(emoji)
    save_favorites(data)
    return jsonify({"status": "added"})

# Удалить из избранного
@app.route("/favorites/<user>", methods=["DELETE"])
def remove_favorite(user):
    data = load_favorites()
    emoji = request.json.get("name")
    if not emoji:
        return jsonify({"error": "No emoji name provided"}), 400
    if user in data and emoji in data[user]:
        data[user].remove(emoji)
        save_favorites(data)
    return jsonify({"status": "removed"})

# AI объяснение эмодзи
@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    data = request.get_json()
    name = data.get("name", "emoji")
    prompt = f"What does the emoji '{name}' usually mean or express? Answer briefly."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": prompt }],
            temperature=0.7
        )
        answer = response["choices"][0]["message"]["content"]
        return jsonify({ "answer": answer })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5050)
