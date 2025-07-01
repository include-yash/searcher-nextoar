from flask import Flask, request, jsonify
import os
import shutil
from flask_cors import CORS
from process_zip import process_folder

app = Flask(__name__)
CORS(app)

@app.route("/process-folders", methods=["POST"])
def process_folders():
    data = request.get_json()
    input_path = data.get("input_path", "").strip()
    destination_path = data.get("destination_path", "").strip()

    if not input_path or not os.path.isdir(input_path):
        return jsonify({"message": f"❌ Invalid input path: '{input_path}'"}), 400

    if not destination_path:
        return jsonify({"message": "❌ Destination path not provided."}), 400

    print(f"\n📂 Input path: {input_path}")
    print(f"📂 Destination path: {destination_path}")

    logs = []

    # Walk ALL leaf subfolders that contain repairTicket_post.txt
    for root, dirs, files in os.walk(input_path):
        if "repairTicket_post.txt" in files:
            print(f"\n🗂 Processing folder with txt: {root}")
            log_output = process_folder(root, destination_path)

            if "Fail IDs Extracted" in log_output:
                logs.append(log_output)
            else:
                print(f"⚠️ Skipped {root} (no fail IDs)")

    if not logs:
        return jsonify({"message": "✅ No folders with valid fail IDs were found."})

    return jsonify({"message": "\n\n".join(logs)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
