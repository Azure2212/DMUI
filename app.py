
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from ACRULE import ACRULE,  classifier1

app = Flask(__name__)
CORS(app) 

@app.route('/')
def home():
    return render_template('UI.html')


subClasses = ['100', "101"] #100 is low risk, 101 is high risk

with open("zheart_disease_risk_dataset_earlymed_keyValue.json", "r") as f:
    mapping = json.load(f)
    
with open("zheart_disease_risk_dataset_earlymed_weightTrained.json", "r") as f:
    data = json.load(f)
rules = []
for item in data:
    rule = ACRULE("","").fromJson(item)
    rules.append(rule)

@app.route('/predict', methods=['POST'])
def predict():
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    
    rs, reason =  classifier1(rules, mapping, subClasses, data)
    return jsonify({
        "message": "JSON received successfully",
        "received_data": reason
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
