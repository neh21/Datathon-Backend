from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
from datetime import datetime
from joblib import load

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Load your models and mapping dict
model = load('decision_tree_model.joblib')
model1 = load('knn_model.joblib')  # Load the KNN model

with open('mapping_dict.json') as f:
    mapping_dict = json.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    date = data['date']
    police_unit = data['policeUnit']

    # Prepare the data
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    day = date_obj.day
    month = date_obj.month
    df = pd.DataFrame({
        'Month': [month] * 24,
        'Day_Offence_From': [day] * 24,
        'District_Name_encoded': [police_unit] * 24,
        'Hour_Offence_From': hours
    })

    # Make predictions
    predictions = model.predict(df).tolist()

    # Format results
    results = [{'hour': hour, 'value': prediction} for hour, prediction in zip(hours, predictions)]
    return jsonify(results)

@app.route('/predict_beat', methods=['POST'])
def predict_beat():
    data = request.get_json()
    year = data['year']
    month = data['month']
    day = data['day']
    unit_name_encoded = data['unit_name_encoded']
    unit_beat_encoded = data['unit_beat_encoded']

    # Prepare the data for model1
    df1 = pd.DataFrame({
        'Year': [year],
        'Month': [month],
        'Day_Offence_From': [day],
        'UnitName_encoded': [unit_name_encoded],
        'Unit_Beat_encoded': [unit_beat_encoded]
    })

    # Make predictions with model1
    patrolling_category_predictions = model1.predict(df1).tolist()

    # Format results
    beat_results = [{'patrolling_category': prediction} for prediction in patrolling_category_predictions]
    return jsonify(beat_results)

if __name__ == '__main__':
    app.run(debug=True)
