import os
import joblib
import numpy as np
import pandas as pd
import glob
import sklearn
import json
import ship_client
import port_client
import ship_port_efficiency_client
import helper_functions
import port_distance_client
from datetime import datetime, timedelta
from flask_cors import CORS

def calculate_final_datetime(initial_datetime, days):
    # Parse the initial datetime string to a datetime object
    initial_datetime = datetime.strptime(initial_datetime, "%Y-%m-%d %H:%M:%S")

    hours = days * 24
    # Calculate the final datetime by adding the specified number of hours
    final_datetime = initial_datetime + timedelta(hours=hours)
    return final_datetime

print("scikit-learn version:", sklearn.__version__)

from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app, origins="*")

def get_eta_between_ports(origin_port_name, destination_port_name, ship_imo):
    # Get ship details
    ship = json.loads(ship_client.get_ship_by_imo(ship_imo))
    ship_type = ship["ship_type"]
    dim_A = ship["dim_a"]
    dim_B = ship["dim_b"]

    # Get miscellaneous details
    port_pair = sorted([origin_port_name, destination_port_name])
    accum_distance = port_distance_client.get_route_distance(port_pair[0], port_pair[1])
    efficiency = ship_port_efficiency_client.get_efficiency(ship_imo, origin_port_name)
    origin_port = port_client.get_port_code(origin_port_name)
    destination_port = port_client.get_port_code(destination_port_name)
    geohash = port_client.get_port_geohash(origin_port_name)

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
    result = saved_model.predict(input_data)[0]
    return result

@app.route('/api/v1/eta', methods=['POST'])
def predict_eta():
    # Get the JSON data from the request
    json_data = request.get_json()

    # Extract relevant features
    # array of ports, ship, departure date
    ship_imo = json_data["imo"]
    port_list = json_data["port_list"]
    current_datetime = "2023-10-01 14:30:00"  # Initial datetime in the format YYYY-MM-DD HH:MM:SS

    # Store the result
    segmented_etas = []
    total_eta = 0

    # Sum up the ETAs
    for i in range(0,len(port_list)-1):
        segment_eta = get_eta_between_ports(port_list[i], port_list[i+1], ship_imo)
        segment_eta_datetime = calculate_final_datetime(current_datetime, segment_eta)
        segmented_etas.append(segment_eta_datetime)
        total_eta += segment_eta
        current_datetime = segment_eta_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return segmented_etas

@app.route('/api/v1/ships', methods=['GET'])
def get_all_ships():
    return ship_client.get_all_ships()

@app.route('/api/v1/ports', methods=['GET'])
def get_all_ports():
    return port_client.get_all_ports()

if __name__ == '__main__':
    app.run(debug=True)