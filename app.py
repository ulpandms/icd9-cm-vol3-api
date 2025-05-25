from flask import Flask, make_response, jsonify
import json
from collections import OrderedDict

app = Flask(__name__)

# Load ICD-9 CM Vol 3 data
with open("icd_9_cm_vol3.json") as f:
    icd9_data = json.load(f)

# Root endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "ICD-9 CM Vol 3 API is running.",
        "endpoints": {
            "/icd9/<code>": "Get a specific ICD procedure by code (e.g. 01.01)",
            "/icd9/search/<keywords>": "Search procedure_desc and exclude_procedure by keywords. Use '+' for OR, space for AND."
        }
    })

# Lookup by exact code
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

    error_data = json.dumps({"error": "Code not found"})
    response = make_response(error_data, 404)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

# Keyword search with OR (+) or AND (space)
@app.route("/icd9/search/<keywords>", methods=["GET"])
def search_icd9_by_keywords(keywords):
    # Detect search mode
    if "+" in keywords:
        keyword_list = keywords.lower().split("+")
        match_type = "or"
    else:
        keyword_list = keywords.lower().split()
        match_type = "and"

    results = []

    for entry in icd9_data:
        text = f"{entry.get('procedure_desc', '')} {entry.get('exclude_procedure', '')}".lower()

        if (
            match_type == "or" and any(k in text for k in keyword_list)
        ) or (
            match_type == "and" and all(k in text for k in keyword_list)
        ):
            results.append(OrderedDict([
                ("icd_code_pcs", entry.get("icd_code_pcs")),
                ("procedure_desc", entry.get("procedure_desc")),
                ("exclude_procedure", entry.get("exclude_procedure"))
            ]))

    if results:
        json_data = json.dumps(results, indent=2)
        response = make_response(json_data)
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    return jsonify({"message": f"No results found for keywords: {keywords}"}), 404

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0")
