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

print("scikit-learn version:", sklearn.__version__)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/eta', methods=['POST'])
def predict_eta():
    # Get the JSON data from the request
    json_data = request.get_json()

    # Extract relevant features
    # array of ports, ship, departure date
    ship_imo = json_data["imo"]
    port_list = json_data["port_list"]
    # departure_date = json_data["departure_date"]

    # Get ship details
    ship = json.loads(ship_client.get_ship_by_imo(ship_imo))
    ship_type = ship["ship_type"]
    dim_A = ship["dim_a"]
    dim_B = ship["dim_b"]

    # Calculate the total distance travelled by the ship
    # accum_distance = json_data["accum_distance"] # needs to be calculated from database entries
    accum_distance = helper_functions.calculate_accumulated_distance(json_data["port_list"])

    # Get the efficiency of the ship coming from the incoming port
    # efficiency = json_data["efficiency"] # taken from the database
    port_list = json_data["port_list"]
    port_list_length = len(port_list)
    efficiency = ship_port_efficiency_client.get_efficiency(ship_imo, port_list[port_list_length-2])

    # Get the origin and destination ports
    # destination_port = json_data["destination_port"] # taken from a list of ports
    # origin_port = json_data["origin_port"] # taken from a list of ports
    origin_port = port_client.get_port_code(port_list[0])
    destination_port = port_client.get_port_code(port_list[port_list_length-1])

    # Get the geohash of the origin port
    # geohash = json_data["geohash"] # this is the origin port's coordinates
    geohash = port_client.get_port_geohash(port_list[0])

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
    return ship_client.get_all_ships()

@app.route('/api/v1/ports', methods=['GET'])
def get_all_ports():
    return port_client.get_all_ports()

if __name__ == '__main__':
    app.run(debug=True)