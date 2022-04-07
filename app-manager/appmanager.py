from email.policy import default
import requests
from flask import Flask, redirect, render_template, session, jsonify, request, url_for
from pymongo import MongoClient
from flask_session import Session
from sqlalchemy import false
from werkzeug.utils import secure_filename
import json
import app_zip_validate as azv
import enduser_json_validate as ejv
import kafka_util, file_storage, generate_api, dockerfile_generator
import os
import zipfile
from flask_cors import CORS, cross_origin
import jwt


app = Flask(__name__)
cors = CORS(app)

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



def read_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

constants = read_json("constants.json")


@app.route("/")
@cross_origin()
def hello():
    return render_template("landing_page.html", 
        login=constants["BASE_URL"] + str(constants["PORT"]["AUTH_PORT"]) + constants["ENDPOINTS"]["AUTH_MANAGER"]["login"],
        register=constants["BASE_URL"] + str(constants["PORT"]["AUTH_PORT"]) + constants["ENDPOINTS"]["AUTH_MANAGER"]["register"],
        data_scientist=constants["BASE_URL"] + str(constants["PORT"]["MODEL_PORT"]) + constants["ENDPOINTS"]["AI_MANAGER"]["ai_home"],
        admin=constants["BASE_URL"] + str(constants["PORT"]["SENSOR_PORT"]) + constants["ENDPOINTS"]["SENSOR_MANAGER"]["admin"],
        developer=constants["BASE_URL"] + str(constants["PORT"]["APP_PORT"]) + constants["ENDPOINTS"]["APP_MANAGER"]["developer"],
        user=constants["BASE_URL"] + str(constants["PORT"]["APP_PORT"]) + constants["ENDPOINTS"]["APP_MANAGER"]["user"],
    )


@app.route("/developer")
def dev():
    try:
        print(request.args['jwt'])
        token = request.args['jwt']
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        return render_template("appdeveloper.html",
            home=constants["BASE_URL"] + str(constants["PORT"]["APP_PORT"]) + constants["ENDPOINTS"]["APP_MANAGER"]["home"]
        )
    except:
        return redirect("/")


@app.route("/enduser")
@cross_origin()
def enduser():
    try:
        print(request.args['jwt'])
        token = request.args['jwt']
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        return render_template("enduser.html",
        home=constants["BASE_URL"] + str(constants["PORT"]["APP_PORT"]) + constants["ENDPOINTS"]["APP_MANAGER"]["home"]
        )
    except:
        return redirect("/")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(["zip"])


@app.route("/get_sensor_data", methods=["POST"])
def get_sensor_data():
    print("in get sensor data of app manager")
    req = request.get_json()
    print("request came")
    sensor_instance_id = req["sensor_instance_id"]
    print("sensor instance detected")
    msg = kafka_util.read_from_topic(sensor_instance_id)
    print("message = {}".format(msg))
    return jsonify({"message" : msg[-1]})


@app.route("/get_model_predict", methods=["POST"])
def get_model_predict():
    req = request.get_json()
    resp = requests.post(constants["BASE_URL"] + str(constants["PORT"]["MODEL_PORT"]) + constants["ENDPOINTS"]["AI_MANAGER"]["get_prediction"], json=req).json()
    return resp


##################### Code Clean up ###############

def get_sensor_instances(app_name, sensors, location):
    app_info = AppDB.find_one({ 'app_name': app_name })
    sensors_list = req_sess.get(constants["BASE_URL"] + str(constants["PORT"]["SENSOR_PORT"]) + constants["ENDPOINTS"]["SENSOR_MANAGER"]["list_sensor_info_by_loc"]).json()
    print(sensors_list)
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
        return {'status_code': 500, 'message': 'No sensors available'}
    else:
        return {'status_code': 200, 'final_instances': list(final_instances)}


def dockerize_app(app_name, location):
    pass


def generate_api_file(model_list, sensor_instances, location, folder, app_name):

    print(model_list, sensor_instances, location, folder, app_name)
    if (generate_api.generate_api(model_list, sensor_instances, location, folder, app_name)):
        # dockerfile_generator.generate_docker_file(folder)
        # os.system('docker build -t '+ app_name + ':latest' + folder+'/Dockerfile')
        # os.system('docker save '+app_name+':latest | gzip > '+app_name+'_latest.tar.gz')

        # file_storage.upload_file('docker_image', app_name+'_latest.tar.gz', app_name+'_latest.tar.gz')
        
        AppInstanceDb.insert_one({
            "location": location,
            # "docker_image": app_name+'_latest.tar.gz'
            "docker_image": folder+'/'+app_name,
            "node_id" : None,
        })

        app_ins_id = str(AppInstanceDb.find_one({
            "location": location,
            # "docker_image": app_name+'_latest.tar.gz'
            "docker_image": folder+'/'+app_name,
        })['_id'])

        print(app_ins_id)

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


@app.route("/deploy_app", methods=['POST'])
def deploy_app():
    '''
    Sends app deployment info to Scheduler
    '''
    req = request.get_json()
    print(req)

    app_name = req["app_name"]
    location = req["location"]
    start_time= req["start_time"]
    duration= req["duration"]
    standalone = req["standalone"]

    app = AppDB.find_one({ 'app_name': app_name })
    if app == None:
        return jsonify({ "status_code": 500, "message": "App does not exist." })
    print(app)
    print("$$$$$$$$$$$$$$$$$$$$",app_name, app["sensors"], location)
    sensor_instances_list = get_sensor_instances(app_name, app['sensors'], location)
    print("####################",sensor_instances_list)
    if sensor_instances_list['status_code'] == 500:
        return jsonify({
            "status_code": 500,
            "message": sensor_instances_list["message"]
        })
    else:
        sensor_instances_list = sensor_instances_list["final_instances"]
    app_inst_id = generate_api_file(app['models'], sensor_instances_list, location, os.getcwd(), app_name) # Make Folder and appname dynamic
    print("********************",app_inst_id)
    # file_storage.download_file("Application_Package", app_name+'_latest.tar.gz', app_name+'.zip')

    if app_inst_id == None:
        return jsonify({
            "status_code": 500,
            "message": "unable to deploy"
        })
    
    # zip_ref = zipfile.ZipFile("Test1.zip")
    # dir_name = "temp/"
    # os.mkdir(dir_name, mode=0o777)
    # os.chdir(dir_name)
    # zip_ref.extractall(dir_name)
    # zip_ref.close()
    # os.chdir("../")

    # os.system("")


    payload = {
        "app_inst_id" : app_inst_id,
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
@app.route("/get_available_resources", methods=['GET'])
def get_available_resources():
    """
    This will return the available Models, Sensors type, and Controllers
    """
    resp = {
        "models": list(),
        "sensors": list(),
        # "controllers": list()
    }

    model_uri = constants["BASE_URL"] + str(constants["PORT"]["MODEL_PORT"]) + constants["ENDPOINTS"]["AI_MANAGER"]["get_model_list"]
    sensor_uri = constants["BASE_URL"] + str(constants["PORT"]["SENSOR_PORT"]) + constants["ENDPOINTS"]["SENSOR_MANAGER"]["sensor_info"]
    
    print(model_uri, sensor_uri)

    model_list = req_sess.get(model_uri).json()
    resp["models"] = model_list

    sensor_info_list = req_sess.get(sensor_uri).json()
    resp["sensors"] = sensor_info_list

    print(resp)
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
        print(file.filename)
        file.save(file.filename)


        config = azv.validate_zip(file.filename)

        model_uri = constants["BASE_URL"] + str(constants["PORT"]["APP_PORT"]) + constants["ENDPOINTS"]["APP_MANAGER"]["get_app_list"]
        existing_app_list = req_sess.get(model_uri).json()

        print(existing_app_list)

        for a in existing_app_list:
            if a['app_name'] == config['app_config']['app_name']:
                return jsonify({"status_code":400, 'message': 'App already exists'})

        models_list = list()
        print(config['app_config']['model_list'], "\n", resources["models"]["model_list"])
        for m in config['app_config']['model_list']:
            for n in resources["models"]["model_list"]:
                if(m['model_name'] == n):
                    models_list.append(n)

        if len(models_list) != len(config['app_config']['model_list']):
            return jsonify({"status_code":400, 'message': 'Model doesnot exist'})

        ##h------------------

        app_name = config['app_config']['app_name']
        print(app_name)
        file_storage.upload_file("Application_Package", app_name+'.zip', file.filename)

        app_info = {
            "app_name": config['app_config']['app_name'],
            "app_author": config['app_config']['app_author'],
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
    os.remove(file.filename)
    return resp


if(__name__ == "__main__"):
    app.run(port=constants["PORT"]["APP_PORT"], debug=True)
