from flask import Flask, request
from numpy import require
import requests
import pymongo
import json

session = requests.Session()
app = Flask(__name__)
myclient=pymongo.MongoClient("mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority")
mydb=myclient["Hackathon"]
mycollection=mydb["Request_db"]

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
            "predict_model": "/predict_model",
            "update_sensor_instance": "/update_sensor_instance"
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

    node_mgr = {
        "app_id" : req["request_id"],
        "end_status":req["end_status"]
        }

    if req["end_status"]==0:
        # print("69 App sent for deployment")

        for x in mycollection.find():
            if str(x['_id'])==req["request_id"]:
                app_path=x['app_path']
                stand_alone=x['stand_alone']
                break
        node_mgr["app_path"]='app_path'
        node_mgr["stand_alone"]='stand_alone'
    # else:
    #     print("80 App sent for termination")
    status = session.post(endpoint['node_manager']['base_url'] + endpoint['node_manager']['uri']['send_to_node_manager'], json=node_mgr).json()
    # status = {"status" : "true"}.json()
    return status


if __name__=="__main__":
    app.run(port=DEPLOYER_PORT, debug=True)