from flask import Flask, jsonify
import json
from collections import OrderedDict

app = Flask(__name__)

# Load ICD-9-CM Volume 3 data from JSON file
with open("icd_9_cm_vol3.json") as f:
    icd9_data = json.load(f)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "ICD-9 CM Vol 3 API is running. Use /icd9/<code> to get procedure description."
    })

@app.route("/icd9/<code>", methods=["GET"])
def get_icd9_description(code):
    for entry in icd9_data:
        if entry.get("icd_code_pcs") == code:
            ordered_entry = OrderedDict([
                ("icd_code_pcs", entry.get("icd_code_pcs")),
                ("procedure_desc", entry.get("procedure_desc")),
                ("exclude_procedure", entry.get("exclude_procedure"))
            ])
            return jsonify(ordered_entry)
    return jsonify({"error": "Code not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0")
