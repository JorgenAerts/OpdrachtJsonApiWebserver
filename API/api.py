"""Code adapted from previous assignments"""""

from fastapi import FastAPI
import requests

# Maak een nieuwe FastAPI-applicatie
app = FastAPI()

URL = "https://my-json-server.typicode.com/JorgenAerts/OpdrachtJsonApiWebserver/sensors"
response = requests.get(URL)  # send a request to the URL to get the sensors list
sensors = response.json()  # Puts the received json data in the sensors variable.

# Root
@app.route('/')
def root():
    return {"message": "Sensor Management API v1.0"}

#Get the list of sensors
@app.get("/sensors")
def get_sensors():
    return sensors  # return all sensors

# Route to get specific sensor
@app.get("/sensors/{sensor_id}")
def get_sensors(sensor_id: int):
        for sensor in sensors:# Look for given id.
            if sensor["id"] == sensor_id:
                return sensor
            return {"message": "Taak niet gevonden"} #Error message

# Add a new sensor        
@app.post("/sensors")
def create_sensor(input: dict):
    new_sensor = {      # Make a new sensor with the next id in the list 
        "id": len(sensors) + 1,
        "name": input["name"],
        "state": input["state"],
        "location": input["location"]
    }
    sensors.append(new_sensor)  #  Add new sensor to the list
    return new_sensor

# Set sensor to active
@app.put("/sensors/activate/{sensor_id}") 
def set_active(sensor_id: int):
    for sensor in sensors:    # Set the sensor with the given id to active
        if sensor["id"] == sensor_id:  
            sensor["state"] = "active" 
            return sensor
    return {"message": "Sensor not found"}  # Error Message

# Set a sensor to inactive
@app.put("/sensors/deactivate/{sensor_id}") 
def set_inactive(sensor_id: int): 
    for sensor in sensors:     # Set the sensor with the given id to inactive
        if sensor["id"] == sensor_id:   
            sensor["state"] = "inactive" 
            return sensor
    return {"message": "Sensor not found"}  # Error Message

# Delete a sensor from the list
@app.delete("/sensors/{sensor_id}")  
def delete_sensor(sensor_id: int):
    global sensors  # The globally declared list of sensors has to be updated to exclude the deleted sensor
    new_list_of_sensors = []  # Make a new empty list
    for sensor in sensors:  # Iterate through the list of sensors
        if sensor["id"] != sensor_id:  # If the given sensor's id is not in the list
            new_list_of_sensors.append(sensor)  # Append the new list of sensors
    sensors = new_list_of_sensors  # Make the newly made list of sensor the current list of sensors
    return {"message": "Sensor deleted"}  # Confirmation message
