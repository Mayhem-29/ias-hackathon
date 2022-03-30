from flask import Flask, request
import requests
import json
import pickle
import numpy as np

sess = requests.Session()

app = Flask(__name__)

SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300

sensor_info = {}
endpoint = {
    "sensor_manager": {
        "base_url": "http://localhost:"+str(SENSOR_PORT), 
        "uri": {
            "sensorinfo": "/sensorinfo",
            "getsensordata": "/getsensordata"
        }
    }, 
    "model_manager": {
        "base_url": "http://localhost:" + str(MODEL_PORT),
        "uri": {
            "list_of_models": "/list_of_models",
            "get_pickle": "/get_pickle",

        }
    }
}


@app.route("/get_sensor_info", methods=["GET"])
def get_sensors_info():
    response_sensor = sess.get(endpoint["sensor_manager"]['base_url'] + endpoint["sensor_manager"]['uri']['sensorinfo']).json()
    response_list = []
    for i in response_sensor.keys():
        response_sensor2 = {}
        response_sensor2["sensor_type_id"] = i
        response_sensor2["sensor_instance"] = []
        for j in response_sensor[i].keys():
            if j == i:
                response_sensor2["sensor_name"] = response_sensor[i][j]
                continue
            temp = {}
            temp["id"] = j
            temp["location"] = response_sensor[i][j]
            response_sensor2["sensor_instance"].append(temp)
        response_list.append(response_sensor2)
    print(response_sensor2)
    return {"response": list(response_list), "status_code": 200}
    # print(response_sensor)


@app.route("/get_model_info", methods=["GET"])
def get_model_info():
    response_model = sess.get(endpoint["model_manager"]['base_url'] + endpoint["model_manager"]['uri']['list_of_models']).json()
    print(response_model)
    return response_model


@app.route("/predict_model", methods=['POST'])
def predict_model():
    # file = open("dummy.json")
    # req = json.load(file)
    req = request.get_json()
    if str(req["tid"]) not in sensor_info.keys():
        return {"output": "Can't deploy", "status_code": 500}
    model_json = {
        "model_name": req["model_name"]
    }
    response_model = sess.post(
        endpoint["model_manager"]['base_url'] + endpoint["model_manager"]['uri']['get_pickle'], json=model_json).json()
    sensor_string = str(req["tid"]) + "," + str(req["location"])
    response_sensor = sess.get(
        endpoint["sensor_manager"]['base_url'] + endpoint["sensor_manager"]['uri']['getsensordata'] + "/" + sensor_string).json()
    # print(response_model)
    # print(type(response_model["pickle_file"]))
    # print(response_sensor)
    model = pickle.load(open(response_model["pickle_file"], "rb"))
    prediction = str(model.predict(
        np.array(response_sensor["data"]).reshape(1, -1))[0])
    ans = {
        "output": prediction,
        "status_code": 200
    }
    return ans


@app.route("/free_instance_by_type_id", methods=['POST'])
def freeinstance_bytypeid():
    # file = open("dummy2.json")
    # request_typeid = json.load(file)
    request_typeid = request.get_json()
    final = []
    if len(request_typeid["sensor_type_id"]) == 0:
        return {"response" : "No type id exists", "status_code" : 500}
    for key in request_typeid["sensor_type_id"]:
        key = str(key)
        if key not in sensor_info.keys():
            return {"response" : "No such type id exists", "status_code" : 500}
        for i in sensor_info[key].keys():
            if sensor_info[key][i][1] == "False":
                temp2 = {}
                temp2["sensor_type_id"] = key
                temp2["sensor_instance_id"] = i
                temp2["sensor_instance_location"] = sensor_info[key][i][0]
                final.append(temp2)
    return {"response" : final , "status_code" : 200}

if __name__ == "__main__":
    resp = sess.get(endpoint["sensor_manager"]['base_url'] + endpoint["sensor_manager"]['uri']['sensorinfo']).json()
    for i in resp.keys():
        sensor_info[i] = {}
        for j in resp[i].keys():
            if i == j:
                continue
            sensor_info[i][j] = []
            sensor_info[i][j].append(resp[i][j])
            sensor_info[i][j].append("False")
    print(sensor_info)
    app.run(port=PLATFORM_PORT, debug=True)
