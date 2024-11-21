""" 
Code adapted from previous exercises

Help with linking location names with sensors, so the data displayed shows the actual names, in stead of their id's
OpenAI, Chatgpt; www.chatgpt.com 18-11-2024

"""

from flask import Flask, render_template
import requests

# Create Flask instance
app = Flask(__name__)

# URLs to get the sensors and locations data
URL1 = "https://my-json-server.typicode.com/JorgenAerts/OpdrachtJsonApiWebserver/sensors"
response = requests.get(URL1)  # send a request to the URL to get the sensors list
sensors = response.json()  # Puts the received json data in the sensors variable.

URL2 = "https://my-json-server.typicode.com/JorgenAerts/OpdrachtJsonApiWebserver/locations"
response = requests.get(URL2)  # send a request to the URL to get the locations list
locations = response.json()  # Puts the received json data in the locations variable.

# Helper function to get the location name by its ID
def get_location_name(location_id):
    for location in locations:
        if location['id'] == location_id:
            return location['location']
    return "Unknown Location"  # If no match is found

# Homepage which links to the other pages
@app.route('/')
def home():
    return render_template("index.html")

# Page with all sensors listed
@app.route("/sensors")
def get_sensors():
    # Render the template with sensors and locations data
    return render_template("sensors.html", title="Sensors", sensors=sensors, locations=locations)

# Page with all locations listed
@app.route("/locations")
def get_locations():
    print(locations)  # Print the locations to verify they are correct
    return render_template("locations.html", title="Locations", locations=locations)

# Page that lists the sensor data from the sensor with the given id
@app.route("/sensors/<int:id>")
def sensor(id):
    # Loop through sensors to find the one with the matching id
    if id < len(sensors):  # Check if the id is valid
        sensor = sensors[id]  # Access the sensor
        location_name = get_location_name(sensor['location'])  # Get location name using location ID
        sensor['location_name'] = location_name  # Add location name to sensor data
        return render_template("sensor.html", sensor=sensor)  # Render the template with the given sensor's data
    else:
        return "Sensor not found.", 404  # Error message if sensor not found

# Page that lists the location with the given id
@app.route("/locations/<int:id>")
def location(id):
    # Loop through locations to find the one with the matching id
    if id < len(locations):  # Check if the id is valid
        location = locations[id]  # Access the location
        # Get all sensors at this location
        location_sensors = [sensor for sensor in sensors if sensor['location'] == location['id']]
        
        # Add location name to each sensor at this location
        for sensor in location_sensors:
            sensor['location_name'] = location['location']
        
        return render_template("location.html", location=location, sensors=location_sensors)  # Render the template with the location data and related sensors
    else:
        return "Location not found.", 404  # Error message if location not found

# Run the Flask app
app.run(host='0.0.0.0', port=5000)
