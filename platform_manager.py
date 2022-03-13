from flask import Flask, request
import requests
import json
import pickle
import numpy as np

sess = requests.Session()

app = Flask(__name__)

sensor_info = {}

@app.route("/get_sensor_info", methods=["GET"])
def get_sensors_info():
    response_sensor = sess.get("http://localhost:8000/sensorinfo").json()
    response_sensor2 = {}
    for i in response_sensor.keys():
        response_sensor2["sensor_id"] = i
        response_sensor2["sensor_instance"] = []
        for j in response_sensor[i].keys():
            temp = {}
            temp["id"] = j
            temp["location"] = response_sensor[i][j]
            response_sensor2["sensor_instance"].append(temp)
    print(response_sensor2)
    return response_sensor2
    # print(response_sensor)
    

@app.route("/get_model_info", methods=["GET"])
def get_model_info():
    response_model = sess.get('http://localhost:8070/list_of_models').json()
    return response_model
    # print(response_model)

@app.route("/predict_model")
def predict_model():
    file = open("dummy.json")
    req = json.load(file)
    # response = request.get_json()
    if str(req["tid"]) not in sensor_info.keys():
        return {"output" : "Can't deploy" , "status_code" : 500}
    model_json = {
        "model_name" : req["model_name"]
    }
    response_model = sess.post('http://localhost:8070/get_pickle', json = model_json).json()
    sensor_string = str(req["tid"]) + "," + str(req["location"])
    response_sensor = sess.get("http://localhost:8000/getsensordata/" + sensor_string).json()
    # print(response_model)
    # print(type(response_model["pickle_file"]))
    # print(response_sensor)
    model = pickle.load(open(response_model["pickle_file"], "rb"))
    prediction = str(model.predict(np.array(response_sensor["data"]).reshape(1,-1))[0])
    ans = {
        "output" : prediction ,
        "status_code" : 200
    }
    return ans

@app.route("/freeinstance_bytypeid")
def freeinstance_bytypeid():
    file = open("dummy2.json")
    request_typeid = json.load(file)
    # request_typeid = request.get_json()
    final = []
    key = str(request_typeid["typeid"])
    if key not in sensor_info.keys():
        return "No such type id exists"
    for i in sensor_info[key].keys():
        if sensor_info[key][i][1] == "False":
            temp2 = {}
            temp2["sensor_type_id"] = request_typeid["typeid"]
            temp2["sensor_instance_id"] = i
            temp2["sensor_instance_location"] = sensor_info[key][i][0]
            final.append(temp2)
    return {"response" : final , "status_code" : 200}

if __name__=="__main__":
    resp = sess.get("http://localhost:8000/sensorinfo").json()
    for i in resp.keys():
        sensor_info[i] = {}
        for j in resp[i].keys():
            sensor_info[i][j] = []
            sensor_info[i][j].append(resp[i][j])
            sensor_info[i][j].append("False")
    print(sensor_info)
    app.run(port=8088, debug=True) 