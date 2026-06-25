from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import json
from datetime import datetime

app = Flask(__name__)

DATA_DIR = os.environ.get('DATA_DIR', '/data')
os.makedirs(DATA_DIR, exist_ok=True)

CONTENT_FILE = os.path.join(DATA_DIR, "content.json")

def load_content():
    if os.path.exists(CONTENT_FILE):
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"text": "", "updated": None}

def save_content(data):
    with open(CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/content", methods=["GET"])
def get_content():
    return jsonify(load_content())

@app.route("/content", methods=["PUT"])
def update_content():
    data = request.get_json()
    content = load_content()
    if "text" in data:
        content["text"] = data["text"]
        content["updated"] = datetime.now().isoformat()
    save_content(content)
    return jsonify(content)

@app.route("/upload-image", methods=["POST"])
def upload_image():
    files = request.files.getlist("files")
    saved = []
    for f in files:
        if f.filename:
            safe_name = os.path.basename(f.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_name = f"{timestamp}_{safe_name}"
            save_path = os.path.join(DATA_DIR, save_name)
            f.save(save_path)
            saved.append(save_name)
    return jsonify({"files_saved": saved})

@app.route("/list")
def list_files():
    files = []
    for f in sorted(os.listdir(DATA_DIR)):
        if f == "content.json":
            continue
        files.append(f)
    content = load_content()
    return jsonify({"files": files, "text": content.get("text", ""), "updated": content.get("updated")})

@app.route("/data/<path:filename>")
def download_file(filename):
    return send_from_directory(DATA_DIR, filename, as_attachment=False)

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    safe_name = os.path.basename(filename)
    file_path = os.path.join(DATA_DIR, safe_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"status": "ok"})
    return jsonify({"status": "not_found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
