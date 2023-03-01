from flask import Flask, request, jsonify, abort
import requests
import json
from datetime import datetime, timedelta, date
import os

API_KEY = os.environ.get('NASA_API_KEY')


app = Flask(__name__)

@app.route('/objects', methods=['GET'])
def get_neos():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    #handling bad inputs – correct datetime format, not None
    if not is_valid_date(start_date_str):
        abort(400, "Invalid start date format")
    
    if not is_valid_date(end_date_str):
        abort(400, "Invalid end date format")
    
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    #handling invalid interval
    if end_date < start_date:
        abort(400, "Invalid interval")

    #all data will be in this list
    objects = []

    #splits the whole interval into 7-day slots
    time_intervals = split_date_interval(start_date, end_date)

    for interval_start, interval_end in time_intervals:
        interval_data = get_objects_in_time_interval(interval_start, interval_end)
        objects+=interval_data

    sorted_objects = sorted(objects, key=lambda x: float(x['distance'].replace(' km', '')))
    return jsonify(sorted_objects), 200

def get_objects_in_time_interval(start, end):

    objects_in_interval = []
    response = requests.get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start}&end_date={end}&api_key={API_KEY}')
    
    if response.status_code != 200:
        abort(response.status_code, f"Error retrieving NEO data: {response.text}")

    # Parse response data to extract NEO information
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        abort(400, "Json error")
    
    try:
        for date in data['near_earth_objects']:
            for neo in data['near_earth_objects'][date]:
                neo_info = {}
                neo_info['name'] = neo['name']
                neo_info['size'] = f"{neo['estimated_diameter']['kilometers']['estimated_diameter_max']:.2f} km"
                neo_info['time'] = neo['close_approach_data'][0]['close_approach_date_full']
                neo_info['distance'] = f"{neo['close_approach_data'][0]['miss_distance']['kilometers']} km"
                objects_in_interval.append(neo_info)
    except KeyError:
        abort(400, "Json key error")

    return objects_in_interval


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


def split_date_interval(start_date, end_date):
    end_date = end_date + timedelta(days=1)
    num_weeks = int((end_date - start_date).days / 7)
    interval_split_points = []
    for i in range(num_weeks + 1):
        interval_split_points.append((start_date + timedelta(weeks=i)))
    interval_split_points.append(end_date)

    intervals = []
    for split_point_index in range(1,len(interval_split_points)):     
        interval_start = interval_split_points[split_point_index-1]
        interval_end = interval_split_points[split_point_index] - timedelta(days=1)

        interval_start_str = interval_start.strftime('%Y-%m-%d')
        interval_end_str = interval_end.strftime('%Y-%m-%d')
        intervals.append((interval_start_str, interval_end_str))

    return intervals

def run():
    if API_KEY is None:
        print('Cannot run server without api key')
        return
    app.run(host='0.0.0.0', port=8001)


if __name__ == '__main__':
    run()
