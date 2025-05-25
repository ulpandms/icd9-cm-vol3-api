from flask import Flask, jsonify
import json

app = Flask(__name__)

with open("icd_codes.json") as f:
    icd_data = json.load(f)

@app.route("/icd/<code>", methods=["GET"])
def get_icd_description(code):
    description = icd_data.get(code.upper())
    if description:
        return jsonify({"code": code.upper(), "description": description})
    return jsonify({"error": "Code not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0")
