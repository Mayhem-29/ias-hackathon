from flask import Flask, request
import requests
import os
import json
from queue import PriorityQueue
from threading import Thread
from datetime import datetime

session = requests.Session()
app = Flask(__name__)

SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300
APP_PORT = 9400
DEPLOYER_PORT = 9500
NODE_PORT = 9500
SCH_PORT = 9600

endpoint = {
    "sensor_manager": {
        "base_url": "http://localhost:"+str(SENSOR_PORT), 
        "uri": {
            "sensorinfo": "/sensorinfo",
            "getsensordata": "/getsensordata"
        }
    },
    "app_manager": {
        "base_url": "http://localhost:" + str(APP_PORT),
        "uri": {
            "get_all_models_sensos": "/get_models_sensors",
            "get_all_apps": "/get_all_applications",
            "get_sensor_by_app_id": "/get_sensor_by_app_id",
            "deploy_app": "/deploy"
        }
    },
    "platform_manager": {
        "base_url": "http://localhost:" + str(PLATFORM_PORT),
        "uri": {
            "get_sensor_info": "/get_sensor_info",
            "get_model_info": "/get_model_info",
            "free_instance_by_type_id": "/free_instance_by_type_id",
            "predict_model": "/predict_model"
        }
    },
    "node_manager": {
        "base_url": "http://localhost:" + str(NODE_PORT),
        "uri": {
            "send_to_node_manager": "/send_to_node_manager",
        }
    },
}


@app.route("/get_schedule_app", methods=["POST"])
def get_schedule_app():
    req = request.get_json()

    sensors_type_id = []
    sensor_instance_list = dict()
    for i in req['sensors']:
        sensors_type_id.append(i['sensor_type_id'])
        sensor_instance_list[i['sensor_type_id']] = list()

    payload = {
        "app_id": req['app_id'],
        "sensors": sensors_type_id
    }

    free_sensor_instances = session.post(endpoint['platform_manager']['base_url'] + endpoint['platform_manager']['uri']['free_instance_by_type_id'], json = payload)
    
    for i in free_sensor_instances:
        if i['sensor_location'] == req['location']:
            sensor_instance_list[i['sensor_type_id']].append(i['sensor_instance_id'])
    
    for i in req['sensors']:
        if(len(sensor_instance_list[i['sensor_type_id']]) < i['n_sensor_instance']):
            status = {"status" : "false"}
            return status
    
    used_sensors = list()

    for i in req['sensors']:
        for j in range(i['n_sensor_instance']):
            used_sensors.append(sensor_instance_list[i['sensor_type_id']][j])
            # function to mark the sensor_instance_list[i['sensor_type_id']][j] as allocated

    node_mgr = {
        "app_id" : req["app_id"],
        "app_path" : req["app_path"],
        "model" : req["model"],
        "location" : req["location"],
        "sensor_instance_list" : used_sensors,
        "end_time" : req["end_time"],
        "sensor_type_id" : sensors_type_id
    }

    status = session.post(endpoint['node_manager']['base_url'] + endpoint['node_manager']['uri']['send_to_node_manager'], json=node_mgr).json()
    # status = {"status" : "true"}.json()
    return status


@app.route("/send_to_node_manager", methods=["POST"])
def send_to_node_manager():
    req = request.get_json()

    # code to add the app instance info to the database

    sensor_dict = dict()

    for i in req["sensor_type_id"]:
        sensor_dict["sensor_type_id"].append(i)

    sensor_dict["location"] = req["location"]

    model_dict = {
        "model_name" : req["model"]
    }

    json_string = json.dumps(sensor_dict)
    with open('sensor_dict.json', 'w') as outfile:
        json.dump(json_string, outfile)

    json_string = json.dumps(model_dict)
    with open('model_dict.json', 'w') as outfile:
        json.dump(json_string, outfile)

    run_command = "python " + req["app_path"] + " sensor_dict.json model_dict.json" 
    os.system("start cmd /k " + run_command)
    status = {"status" : "true"}

    return status

if __name__=="__main__":
    app.run(port=DEPLOYER_PORT, debug=True)