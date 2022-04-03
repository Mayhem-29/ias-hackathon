from email.policy import default
import requests
from flask import Flask, session, jsonify, request
from pymongo import MongoClient
from flask_session import Session
from sqlalchemy import false
from werkzeug.utils import secure_filename
import json
import os
import sys
import zipfile
import app_zip_validate as azv
import enduser_json_validate as ejv


app = Flask(__name__)
app.config['SECRET_KEY'] = "dub_nation"

DB_SERVER = "mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority"
client = MongoClient(DB_SERVER)
HACKATHON_DB = client['Hackathon']

AppDB = HACKATHON_DB['AppInfo'] #application info table is set to AppDB

sess = Session(app)
req_sess = requests.Session()

SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300
APP_PORT = 9400
DEPLOYER_PORT = 9500
NODE_PORT = 9500
SCH_PORT = 9600


ai_manager_endpoints = {
    "base_url": "http://localhost:" + str(MODEL_PORT),
    "uri": {
        "get_model_list": "/all_model_details",
        "model_details": "/model_details",
        "list_models": "/list_models"

    }

}

platform_endpoints = {
    "base_url": "http://localhost:" + str(PLATFORM_PORT),
    "uri": {
        "get_sensor_info": "/get_sensor_info",
        "get_model_info": "/get_model_info",
        "free_instance_by_type_id": "/free_instance_by_type_id",
        "predict_model": "/predict_model"
    }
}

scheduler_endpoints = {
    "base_url": "http://localhost:" + str(SCH_PORT),
    "uri": {
        "deploy_app": "/deploy_app"
    }
}

sensor_manager_endpoints = {
    "base_url":"http://localhost:" + str(SENSOR_PORT),
    "uri":{
        "get_sensor_info": "/newsensorinfo_ap"
    }
}




def read_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)


#DEVELOPER VIEW



@app.route("/get_model_list", methods=["GET"])
def get_model_list():
    '''
    requests AI manager for list of avalaible models with sensor requirement
    '''
    model_list = req_sess.get(ai_manager_endpoints["base_url"] + ai_manager_endpoints["uri"]["get_model_list"]).json()
    return model_list


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(["zip"])



@app.route("/appDevInput", methods=["POST"])
def upload_file():
    '''
    uploads file to server
    '''
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    file = request.files['file']

    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save("uploadfiles/" + filename)
        return jsonify({'message': 'File successfully uploaded'})
    else:
        resp = jsonify({'message': 'Allowed file types are zip'})
        resp.status_code = 400
        return resp

#USER VIEW

dummy_sensor_json= {
    "response": "success",
    "sensor_list": [
    {
        "sensor_type":"A",
        "sensor_location":"xyz",
        "sensor_instances":"3"

    },
    {
        "sensor_type":"B",
        "sensor_location":"xyz",
        "sensor_instances":"2"
    },
    {
        "sensor_type":"A",
        "sensor_location":"adz",
        "sensor_instances":"1"
    },
    {
        "sensor_type":"C",
        "sensor_location":"xyz",
        "sensor_instances":"1"
    }
    ] 
}





'''
@app.route("/newsensorinfo_ap", methods=["GET"])
'''

@app.route("/get_sensor_list", methods=["GET"])
def get_sensor_list():
    '''
    request platform manager for sensor list
    '''
    sensor_info = req_sess.get(sensor_manager_endpoints["base_url"] + sensor_manager_endpoints["uri"]["get_sensor_info"]).json() #kafka
    return sensor_info

@app.route("/get_app_list", methods=["GET"])
def get_app_list():
    '''
    gets available app list from app database
    '''
    app_list = AppDB.find()
    app_list_json = []
    for app in app_list:
        app_list_json.append({
            "app_id": str(app['_id']),
            "app_name": app['app_name']})

    return jsonify(app_list_json)


@app.route("/validate_enduser_config",methods=["POST"])
def validate_enduser_config():
    app_config = request.get_json()


    if not ejv.validate_app_json(app_config):
        return '{"status:500","message":"app_config is not valid"}'

    db_response = AppDB.find_one({"app_name": app_config['app_name']})
    
    if db_response == None:
        return '{"status:500","message":"app_name is not valid"}'

    
    location = app_config["location"]
    sensor_inf= get_sensor_list()

    if not ejv.UserSensorValidation(sensor_inf, db_response, location):
        return '{"status:500","message":"sensor_config is not valid"}'
    
    return '{"status:200","message":"app_config is valid"}'

#SCHEDULER

'''
scheduler json
{
    "app_path" : "some_app_path",
    "start_time" : "some_start_time",
    "duration" : "some_duration_app",
    "standalone" : "true/false"
}
'''

#@app.route("/schedule_app", methods=["POST"])
def deploy_app():
    '''
    Sends app deployment info to Scheduler
    '''
    app_info = request.get_json()
    app_name = app_info["app_name"]
    app_path = app_info["app_path"]
    app_start_time= app_info["start_time"]
    app_duration= app_info["duration"]
    app_standalone = app_info["standalone"]
    app_info = {
        "app_path": app_path,
        "start_time": app_start_time,
        "duration": app_duration,
        "standalone": app_standalone
    }
    #change with kafka
    response = req_sess.post(scheduler_endpoints["base_url"] + scheduler_endpoints["uri"]["deploy_app"], json=app_info) 
    return response.text


if(__name__ == "__main__"):
    app.run(port=APP_PORT, debug=True)
