
""" Code adapted from previous excercises"""

from flask import Flask, render_template
import requests
# Create Flask instance
app = Flask(__name__)

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

# Page with that lists the sensor data from the sensor with the given id
@app.route("/sensors/<int:id>")
def sensor(id):
    URL = f"https://my-json-server.typicode.com/JorgenAerts/OpdrachtJsonApiWebserver/sensors/{id}"
    response = requests.get(URL)  # send a request to the URL to get the sensors list
    sensors = response.json()  # Puts the received json data in the sensors variable.
    if id < len(sensors):  # Check if the given id is not over the number of sensors and thus invalid
        sensor = sensors[id]  # Makes the given id's sensor a variable
        return render_template("sensor.html", sensor=sensor )  # Render the template for the sensor page
    else:
        return "No sensors found .", 404  # Error message
    
app.run(host='0.0.0.0', port=5000)