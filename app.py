from flask import Flask, make_response
import json
from collections import OrderedDict

app = Flask(__name__)

with open("icd_9_cm_vol3.json") as f:
    icd9_data = json.load(f)

@app.route("/icd9/<code>", methods=["GET"])
def get_icd9_description(code):
    for entry in icd9_data:
        if entry.get("icd_code_pcs") == code:
            ordered_entry = OrderedDict([
                ("icd_code_pcs", entry.get("icd_code_pcs")),
                ("procedure_desc", entry.get("procedure_desc")),
                ("exclude_procedure", entry.get("exclude_procedure"))
            ])
            json_data = json.dumps(ordered_entry, indent=2)
            response = make_response(json_data)
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
    # fallback
    error_data = json.dumps({"error": "Code not found"})
    response = make_response(error_data, 404)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0")
