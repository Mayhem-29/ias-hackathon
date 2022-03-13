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
    return response_sensor
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
    if req["tid"] not in sensor_info.keys():
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
    request_typeid = request.get_json()
    final = []
    if request_typeid["typeid"] not in sensor_info.keys():
        return "No such type id exists"
    for i in sensor_info[request_typeid["typeid"]].keys():
        if sensor_info[request_typeid["typeid"]][i][1] == "False":
            final.append(i)
    return {"response" : final}

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