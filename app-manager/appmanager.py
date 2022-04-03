from email.policy import default
import requests
from flask import Flask, session, jsonify, request
from pymongo import MongoClient
from flask_session import Session
from sqlalchemy import false
from werkzeug.utils import secure_filename
import json
import app_zip_validate as azv
import enduser_json_validate as ejv
import kafka_util, file_storage, generate_api, dockerfile_generator
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "dub_nation"

DB_SERVER = "mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority"
client = MongoClient(DB_SERVER)
HACKATHON_DB = client['Hackathon']

AppDB = HACKATHON_DB['AppInfo'] #application info table is set to AppDB
AppInstanceDb = HACKATHON_DB['AppInstance']

sess = Session(app)
req_sess = requests.Session()

SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300
APP_PORT = 9400
DEPLOYER_PORT = 9500
NODE_PORT = 9500
SCH_PORT = 9600


# ai_manager_endpoints = {
#     "base_url": "http://localhost:" + str(MODEL_PORT),
#     "uri": {
#         "get_model_list": "/all_model_details",
#         "model_details": "/model_details",
#         "list_models": "/list_models"
#     }

# }

# platform_endpoints = {
#     "base_url": "http://localhost:" + str(PLATFORM_PORT),
#     "uri": {
#         "get_sensor_info": "/get_sensor_info",
#         "get_model_info": "/get_model_info",
#         "free_instance_by_type_id": "/free_instance_by_type_id",
#         "predict_model": "/predict_model"
#     }
# }


# scheduler_endpoints = {
#     "base_url": "http://localhost:" + str(SCH_PORT),
#     "uri": {
#         "deploy_app": "/deploy_app"
#     }
# }


# sensor_manager_endpoints = {
#     "base_url":"http://localhost:" + str(SENSOR_PORT),
#     "uri":{
#         "get_sensor_info": "/newsensorinfo_ap"
#     }
# }


def read_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

constants = read_json("constants.json")

#DEVELOPER VIEW

<<<<<<< HEAD
# @app.route("/get_model_list", methods=["GET"])
# def get_model_list():
#     '''
#     requests AI manager for list of avalaible models with sensor requirement
#     '''
#     model_list = req_sess.get(ai_manager_endpoints["base_url"] + ai_manager_endpoints["uri"]["get_model_info"]).json()
#     return model_list
=======


@app.route("/get_model_list", methods=["GET"])
def get_model_list():
    '''
    requests AI manager for list of avalaible models with sensor requirement
    '''
    model_list = req_sess.get(ai_manager_endpoints["base_url"] + ai_manager_endpoints["uri"]["get_model_list"]).json()
    return model_list
>>>>>>> 2c0272f72f2b74914932823881c073861593b5fa


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(["zip"])


# @app.route("/app_dev_upload", methods=["POST"])
# def upload_file():
#     '''
#     uploads file to server
#     '''
#     if 'file' not in request.files:
#         resp = jsonify({'message': 'No file part in the request'})
#         resp.status_code = 400
#         return resp

#     file = request.files['file']

#     if file.filename == '':
#         resp = jsonify({'message': 'No file selected for uploading'})
#         resp.status_code = 400
#         return resp
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save("uploadfiles/" + filename)
#         return jsonify({'message': 'File successfully uploaded'})
#     else:
#         resp = jsonify({'message': 'Allowed file types are zip'})
#         resp.status_code = 400
#         return resp






# '''
# @app.route("/newsensorinfo_ap", methods=["GET"])
# '''

# @app.route("/get_sensor_list", methods=["GET"])
# def get_sensor_list():
#     '''
#     request platform manager for sensor list
#     '''
#     sensor_info = req_sess.get(sensor_manager_endpoints["base_url"] + sensor_manager_endpoints["uri"]["get_sensor_info"]).json() #kafka
#     return sensor_info



# @app.route("/validate_enduser_config",methods=["POST"])
# def validate_enduser_config():
#     app_config = request.get_json()


#     if not ejv.validate_app_json(app_config):
#         return '{"status:500","message":"app_config is not valid"}'

#     db_response = AppDB.find_one({"app_name": app_config['app_name']})
    
#     if db_response == None:
#         return '{"status:500","message":"app_name is not valid"}'

    
#     location = app_config["location"]
#     sensor_inf= get_sensor_list()

#     if not ejv.UserSensorValidation(sensor_inf, db_response, location):
#         return '{"status:500","message":"sensor_config is not valid"}'
    
#     return '{"status:200","message":"app_config is valid"}'

# #SCHEDULER

# '''
# scheduler json
# {
#     "app_path" : "some_app_path",
#     "start_time" : "some_start_time",
#     "duration" : "some_duration_app",
#     "standalone" : "true/false"
# }
# '''

# #@app.route("/schedule_app", methods=["POST"])
# def deploy_app():
#     '''
#     Sends app deployment info to Scheduler
#     '''
#     app_info = request.get_json()
#     app_name = app_info["app_name"]
#     app_path = app_info["app_path"]
#     app_start_time= app_info["start_time"]
#     app_duration= app_info["duration"]
#     app_standalone = app_info["standalone"]
#     app_info = {
#         "app_path": app_path,
#         "start_time": app_start_time,
#         "duration": app_duration,
#         "standalone": app_standalone
#     }
#     #change with kafka
#     response = req_sess.post(scheduler_endpoints["base_url"] + scheduler_endpoints["uri"]["deploy_app"], json=app_info) 
#     return response.text


@app.route("/get_sensor_data", methods=["POST"])
def get_sensor_data():
    req = request.get_json()
    sensor_instance_id = req["sensor_instance_id"]
    msg = kafka_util.read_from_topic(sensor_instance_id)
    return msg[-1]


@app.route("/get_model_predict", methods=["POST"])
def get_model_predict():
    req = request.get_json()
    data = req['data']
    resp = requests.post(constants["BASE_URL"] + str(constants["PORT"]["MODEL_PORT"]) + constants["ENDPOINTS"]["AI_MANAGER"]["get_prediction"], json=data).json()
    return resp


##################### Code Clean up ###############

def get_sensor_instances(app_name, sensors, location):
    app_info = AppDB.find_one({ 'app_name': app_name })
    sensors_list = req_sess.get(constants["BASE_URL"] + str(constants["PORT"]["SENSOR_PORT"]) + constants["ENDPOINTS"]["SENSOR_MANAGER"]["list_sensor_info_by_loc"]).json()
    
    sensor_instance_list = list()
    final_instances = set()

#filter by locaion
    for obj in sensors_list['resp']:
        if obj['location'] == location:
            sensor_instance_list.append(obj)

    for sensor in sensors:
        for ins in sensor_instance_list:
            if(ins['sensor_type'] == sensor['sensor_type']):
                if len(ins['sensor_ins']) == 0:
                    return jsonify({ 'status_code': 500, 'message': 'No sensors available' })
                else:
                    for i in ins['sensor_ins']:
                        if i not in final_instances:
                            final_instances.add(i)
    
    if len(final_instances) != len(sensors):
        return jsonify({ 'status_code': 500, 'message': 'No sensors available' })
    else:
        return jsonify({ 'status_code': 200, 'final_instances': final_instances })


def dockerize_app(app_name, location):
    pass


def generate_api_file(model_list, sensor_instances, location, folder, app_name):

    if generate_api(model_list, sensor_instances, location, folder+'/'+app_name) == True:
        dockerfile_generator.generate_docker_file(folder)
        os.system('docker build -t '+ app_name + ':latest' + folder+'/Dockerfile')
        os.system('docker save '+app_name+':latest | gzip > '+app_name+'_latest.tar.gz')

        file_storage.upload_file('docker_image', app_name+'_latest.tar.gz', app_name+'_latest.tar.gz')
        AppInstanceDb.insert_one({
            "location": location,
            "docker_image": app_name+'_latest.tar.gz'
        })

        app_ins_id = AppInstanceDb.find({
            "location": location,
            "docker_image": app_name+'_latest.tar.gz'
        })['_id']

        return app_ins_id
    else:
        return None




#USER

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


@app.route("/deploy_app")
def deploy_app():
    '''
    Sends app deployment info to Scheduler
    '''
    req = request.get_json()

    app_name = req["app_name"]
    location = req["location"]
    start_time= req["start_time"]
    duration= req["duration"]
    standalone = req["standalone"]

    app = AppDB.find_one({ 'app_name': app_name })
    sensor_instances_list = get_sensor_instances(app_name, app['sensors'], location)
    app_inst_id = generate_api_file(app['models'], sensor_instances_list, location, "test/", app_name)

    if app_inst_id == None:
        return jsonify({
            "status_code": 500,
            "message": "unable to deploy"
        })

    payload = {
        "app_inst_id" : "",
        "start_time": start_time,
        "end_time": duration,
        "stand_alone": standalone #bool
    }
    #change with kafka
    response = req_sess.post(constants["BASE_URL"] + str(constants["PORT"]["SCH_PORT"]) + constants["ENDPOINTS"]["SCHEDULER_MANAGER"]["deploy_app"], json=payload) 
    return {
        "status_code": 200,
        "message": response.text
    }


#DEV
@app.route("/get_available_resources")
def get_available_resources():
    """
    This will return the available Models, Sensors type, and Controllers
    """
    resp = {
        "models": list(),
        "sensors": list(),
        "controllers": list()
    }

    model_list = req_sess.get(constants["BASE_URL"] + str(constants["PORT"]["MODEL_PORT"]) + constants["ENDPOINTS"]["AI_MANAGER"]["get_model_list"]).json()
    resp["models"] = model_list

    sensor_info_list = req_sess.get(constants["BASE_URL"] + str(constants["PORT"]["SENSOR_PORT"]) + constants["ENDPOINTS"]["SENSOR_MANAGER"]["sensor_info"]).json()
    resp["sensors"] = sensor_info_list

    #Controllers to be added later

    return resp


@app.route("/upload_application", methods=["POST"])
def upload_application():
    '''
    This will allow App Developer to upload their zip file containing
    Applications related files: 
        app_config.json, sensor_type_config.json, controller_type.json
        source code, requirements.txt as App.zip

    '''

    resp = dict()

    # if 'file' not in request.files:
    #     resp = {"status_code":400, 'message': 'No file part in the request'}
    #     return resp

    file = request.files['file']

    # if file.filename == '':
    #     resp = {"status_code":400, 'message': 'No file selected for uploading'}
    #     return resp
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        resources = get_available_resources()
        config = azv.validate_zip(file.filename)
        existing_app_list = get_app_list()
        
        for a in existing_app_list:
            if a['app_name'] == config['app_config']['app_name']:
                return jsonify({"status_code":400, 'message': 'App already exists'})

        models_list = list()
        
        for m in config['app_config']['model_list']:
            for n in resources["models"]:
                if(m['model_name'] == n['model_name']):
                    models_list.append(n)

        if len(models_list) != len(config['app_config']['model_list']):
            return jsonify({"status_code":400, 'message': 'Model doesnot exist'})

        ##h------------------

        app_name = config['app_config']['app_name']
        file.save("tmp/" + filename)
        file_storage.upload_file("application/"+app_name+'/','App.zip', "tmp/" + filename)

        app_info = {
            "app_name": config['app_config']['app_name'],
            "app_author": config['app_config']['app_author'],
            "app_path": "azure path",
            "models": models_list,
            "sensors": config['sensor_type_config']
        }

        AppDB.insert_one(app_info)

        resp = {
            "status_code": 200,
            'message': 'File successfully uploaded'
        }
    else:
        resp = {"status_code":400, 'message': 'Allowed file types are zip'}
    
    return resp


if(__name__ == "__main__"):
<<<<<<< HEAD
    app.run(port=constants["PORT"]["APP_PORT"], debug=True)
=======
    app.run(port=APP_PORT, debug=True)
>>>>>>> 2c0272f72f2b74914932823881c073861593b5fa
