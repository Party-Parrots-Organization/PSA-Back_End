import requests
import json
from datetime import datetime
import re
import math

def change_time_to_midnight(iso_datetime_str):
    # Extract the date portion and append the time '00:00:00Z'
    date_portion = re.match(r'\d{4}-\d{2}-\d{2}', iso_datetime_str).group()
    return f"{date_portion}T10:00:00Z"

def get_weather_record_by_time(weather_list, target_time):
    for weather_data in weather_list:
        if weather_data['time'] == target_time:
            return weather_data

def euclidean_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def get_nearest_valid_point(x, y):
    points = [
        [42.3478, -71.0466], [33, -84]
    ]
    # Return the nearest valid point
    lat, lon = 0, 0
    min_distance = float('inf')
    for point in points:
        current_distance = euclidean_distance(x, y, point[0], point[1])
        if (current_distance < min_distance):
            min_distance = current_distance
            lat, lon = point[0], point[1]
    return lat, lon

def get_weather_severity(weather_code):
    # Weather Categories:
    # 0: Good
    # 1: Moderately Bad
    # 2: Very Bad
    weather_categories = {
        0 : [1000, 1100, 1101, 1103, 1102, 2100, 2101, 2102, 2106, 2107, 2108,
                4203, 4205, 4213, 4214, 4215],
        9 : [4000, 4200, 4204, 4208, 5100, 5102, 5103, 5104, 
                        5105, 5106, 5107, 6000, 6003, 6002, 6004, 6200,
                        6213, 6214, 6215],
        28 : [8000, 8001, 8002, 8003]
    }
    # Iterate through weather categories and determine severity
    for severity, codes in weather_categories.items():
        if weather_code in codes:
            return severity

    # Return -1 for unknown weather code
    return 0

def get_weather(datetime_str, lat, lon):
    print("IN WEATHER CLIENT")
    print("values", datetime_str, lat, lon)
    try:
        # Get the nearest point
        lat, lon = get_nearest_valid_point(lat, lon)
    
        # Parse the original date and time
        original_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        # Reformat to ISO 8601 format
        iso8601_datetime_str = original_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Change to midnight to get the daily forecast
        midnight_iso_datetime_str = change_time_to_midnight(iso8601_datetime_str)
        
        # Construct the request url
        base_url = "https://api.tomorrow.io/v4/weather/forecast"
        
        location = f"{lat:.4f},{lon:.4f}"
        api_key = "v3kSMKP59Eq5aIgpG8KCtZ8t1Z6vjOGA"

        # Construct the full URL with query parameters
        url = f"{base_url}?location={location}&apikey={api_key}"

        # Make the request
        print("MIDNIGHT STRING", midnight_iso_datetime_str)
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        print(response)
        response = json.loads(response.text)
        daily_responses = response["timelines"]["daily"]
        record = get_weather_record_by_time(daily_responses, midnight_iso_datetime_str)["values"]
        weather_delay = get_weather_severity(record["weatherCodeMax"])

        print("IN WEATHER CLIENT RESPONSE")
        print("DELAY", weather_delay)
        return({
            "windSpeedAvg": record["windSpeedAvg"],
            "windDirectionAvg": record["windDirectionAvg"],
            "visibilityAvg": record["visibilityAvg"],
            "temperatureAvg": record["temperatureAvg"],
            "dewPointAvg": record["dewPointAvg"],
            "humidityAvg": record["humidityAvg"],
            "pressureSurfaceLevelAvg": record["pressureSurfaceLevelAvg"],
            "weatherCodeMax": record["weatherCodeMax"],
            "rainIntensityAvg": record["rainIntensityAvg"],
            "sleetIntensityAvg": record["sleetIntensityAvg"],
            "snowIntensityAvg": record["snowIntensityAvg"],
            "cloudCoverAvg": record["cloudCoverAvg"],
            "weatherDelay": weather_delay
        })
    except Exception as e:
        return str(e)

# print(get_weather("2023-10-01 14:30:00", 42.3478, -71.0466))
print(get_weather("2023-10-01 14:30:00", 30.0, 122.0))
# 2023-10-12 15:40:10