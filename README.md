# Nasa-api

## Assignment
Create a simple Python web application with a single REST endpoint that takes two date arguments and retrieves the list of near-Earth space objects approaching Earth in that time interval. Output the list of the objects, sorted by their closest approach distance, containing  the object name, size estimate, time and distance of the closest encounter.

The data should come from the API of NeoWs service at https://api.nasa.gov/ (free registration required). The application should also properly handle data ranges larger than the 7-day limit imposed by the Nasa API.

Be prepared to explain how the application works, including the data formats and network protocols used.

REST API endpoint:
* GET /objects
* query parameter 'start_date' in format YYYY-MM-DD
* query parameter 'end_date' in format YYYY-MM-DD
* returns JSON array of JSON objects

Implementation:
* Python 3, web framework of your choice (FastAPI, Flask, Django, etc)
* Include a Dockerfile

## Usage
- Paste your API key into settings.py
- Run 'docker-compose up' in the root of the repository It will launch a web application on 127.0.0.1:8001 
-> It will handle the endpoint described in the assignment
- Eventually you can use only the Dockerfile

## Testing 
- to run tests, run 'python3 run_tests.py'
- some basic tests implemented (handling bad requests, correct output for valid request)

## Implementation details
- Flask framework used
