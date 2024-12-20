"""
Code adapted from previous assignments
ChatGPT helped me with updating the json file remotely.(request.put, request.post and request.delete)
and with the last block so it would run properly.
OpenAI, ChatGPTv4 www.chatgpt.com 15-11-2024

"""""

from fastapi import FastAPI
import requests

# Make a  FastAPI-application
app = FastAPI()

URL = "https://my-json-server.typicode.com/JorgenAerts/OpdrachtJsonApiWebserver/sensors"
response = requests.get(URL)  # send a request to the URL to get the sensors list
sensors = response.json()  # Puts the received json data in the sensors variable.

# Root
@app.get('/')
def root():
    return {"message": "Sensor Management API v1.0"}

#Get the list of sensors
@app.get("/sensors")
def get_sensors():
    return sensors  # return all sensors

#Get the list of sensors
@app.get("/locations")
def get_locations():
    URL = "https://my-json-server.typicode.com/JorgenAerts/OpdrachtJsonApiWebserver/locations"
    response = requests.get(URL)  # send a request to the URL to get the locations list
    locations = response.json()  # Puts the received json data in the locations variable.
    return locations  # return all slocations

# Route to get specific sensor
@app.get("/sensors/{sensor_id}")
def get_sensor(sensor_id: int):
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
    requests.post(URL, json=new_sensor)  # Post the new sensor to the json file. 
    return new_sensor

# Set sensor to active
@app.put("/sensors/activate/{sensor_id}") 
def set_active(sensor_id: int):
    for sensor in sensors:    # Set the sensor with the given id to active
        if sensor["id"] == sensor_id:  
            sensor["state"] = "active"
            requests.put(f"{URL}/{sensor_id}", json={"state": "active"})   # Update the json file
            return sensor
    return {"message": "Sensor not found"}  # Error Message

# Set a sensor to inactive
@app.put("/sensors/deactivate/{sensor_id}") 
def set_inactive(sensor_id: int): 
    for sensor in sensors:     # Set the sensor with the given id to inactive
        if sensor["id"] == sensor_id:   
            sensor["state"] = "inactive"
            requests.put(f"{URL}/{sensor_id}", json={"state": "inactive"})  # Updates the json file
            return sensor
    return {"message": "Sensor not found"}  # Error Message

# Delete a sensor from the list
@app.delete("/sensors/{sensor_id}")  
def delete_sensor(sensor_id: int):
    global sensors # use the list of sensors globaly defined
    new_list_of_sensors = []  # Make a new empty list
    for sensor in sensors:  # Iterate through the list of sensors
        if sensor["id"] != sensor_id:  # If the given sensor's id is not in the list
            new_list_of_sensors.append(sensor)  # Append the new list of sensors
    sensors = new_list_of_sensors  # Make the newly made list of sensor the current list of sensors
    requests.delete(f"{URL}/{sensor_id}")  # update json file
    return {"message": "Sensor deleted"}  # Confirmation message

# This block came from ChatGPT, the program would not run without it
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("management:app", host="127.0.0.1", port=8000, reload=True)