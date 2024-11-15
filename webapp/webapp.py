
""" Code adapted from previous excercises"""

from flask import Flask, render_template
import requests
# Create Flask instance
app = Flask(__name__)

URL = "https://my-json-server.typicode.com/JorgenAerts/OpdrachtJsonApiWebserver/sensors"
response = requests.get(URL)  # send a request to the URL to get the sensors list
sensors = response.json()  # Puts the received json data in the sensors variable.

# Homepage which links to the other pages
@app.route('/')
def home():
    return render_template("index.html")

@app.route("/sensors")
def get_sensors():
    URL = "https://my-json-server.typicode.com/JorgenAerts/OpdrachtJsonApiWebserver/sensors"
    response = requests.get(URL)  # send a request to the URL to get the sensors list
    sensors = response.json()  # Puts the received json data in the sensors variable.
    return render_template("sensors.html", title="Sensors", sensors=sensors)

@app.route("/locations")
def get_locations():
    URL = "https://my-json-server.typicode.com/JorgenAerts/OpdrachtJsonApiWebserver/locations"
    response = requests.get(URL)  # send a request to the URL to get the sensors list
    locations = response.json()  # Puts the received json data in the sensors variable.
    return render_template("locations.html", title="Locations", locations=locations)

# Page with that lists the sensor data from the sensor with the given id
@app.route("/sensors/<int:id>")
def sensor(id):    
    # Loop through sensors to find the one with the matching id
    if id < len(sensors):  # check if the id is valid.
        sensor = sensors[id]  # Access the sensor
        return render_template("sensor.html", sensor=sensor) # render the template with the given sensor's data
    else:
        return "Sensor not found.", 404  # Error message
app.run(host='0.0.0.0', port=5000)