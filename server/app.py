import os
import joblib
import numpy as np
import pandas as pd
import glob
import sklearn
import json
import db_client

print("scikit-learn version:", sklearn.__version__)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/eta', methods=['POST'])
def predict_eta():
    # Get the JSON data from the request
    json_data = request.get_json()

    # Extract relevant features
    ship_imo = json_data["imo"]
    accum_distance = json_data["accum_distance"]
    efficiency = json_data["efficiency"]
    geohash = json_data["geohash"]
    ship_type = json_data["ship_type"]
    dim_B = json_data["dim_B"]
    destination_port = json_data["destination_port"]
    dim_A = json_data["dim_A"]
    origin_port = json_data["origin_port"]

    # Create a dictionary from the extracted values
    data = {
        "accum_distance": [accum_distance],
        "efficiency": [efficiency],
        "geohash": [geohash],
        "ship_type": [ship_type],
        "dim_B": [dim_B],
        "destination_port": [destination_port],
        "dim_A": [dim_A],
        "origin_port": [origin_port]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Create a NumPy array
    input_data = df[['accum_distance', 'efficiency', 'geohash', 'ship_type', 'dim_B', 'destination_port', 'dim_A', 'origin_port']].values

    # Load the saved model
    saved_model = joblib.load("./best_model.joblib")

    # Make predictions using the saved model
    result = saved_model.predict(input_data)

    # Convert NumPy array to a JSON-serializable format
    result_json = json.dumps(result.tolist())

    return jsonify(result_json)

@app.route('/api/v1/ships', methods=['GET'])
def get_all_ships():
    return db_client.get_all_ships()

@app.route('/api/v1/ports', methods=['GET'])
def get_all_ports():
    return db_client.get_all_ports()

if __name__ == '__main__':
    app.run(debug=True)