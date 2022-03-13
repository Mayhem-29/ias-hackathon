from email.policy import default
import requests
from flask import Flask, session, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = "dub_nation"

username = "root"
password = "Root1234"
server = "localhost:3306"
database = "platformdb"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{server}/{database}"
app.config['SESSION_TYPE'] = "sqlalchemy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db
sess = Session(app)
req_sess = requests.Session()

SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300
APP_PORT = 9400
DEPLOYER_PORT = 9500
NODE_PORT = 9500
SCH_PORT = 9600

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
        "deploy": "/"
    }
}

class AppInfo(db.Model):
    
    app_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    app_name = db.Column(db.String(80), nullable=False)
    run_type = db.Column(db.String(80), nullable=False, default="ondemand")
    app_path = db.Column(db.String(100), nullable=False)

    def __init__(self, app_name, run_type):
        self.app_name = app_name
        self.run_type = run_type


class AppSensorMapping(db.Model):
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    app_id = db.Column(db.Integer, nullable=False)
    sensor_id = db.Column(db.Integer, nullable=False)
    n_sensor_instance = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, app_id, sensor_id):
        self.app_id = app_id
        self.sensor_id = sensor_id


class AppModelMapping(db.Model):
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    app_id = db.Column(db.Integer, nullable=False)
    model_id = db.Column(db.String(80), nullable=False)

    def __init__(self, app_id, model_id):
        self.app_id = app_id
        self.model_id = model_id


# To Developers
@app.route("/get_models_sensors", methods=['GET'])
def get_models_sensors():

    models = req_sess.get(platform_endpoints["base_url"] + platform_endpoints["uri"]["get_model_info"]).json()
    print(models)
    if models['status_code'] != 200:
        return {
            "status": False,
            "message": "Something went wrong with model"
        }

    model_list = list()
    for m in models['model_list']:
        model_list.append({
            "model_name": m
        })
    
    sensors = req_sess.get(platform_endpoints["base_url"] + platform_endpoints["uri"]["get_sensor_info"]).json()
    sensor_list = list()
    for s in sensors['response']:
        sensor_list.append({
            "sensor_type_id": s['sensor_type_id'],
            "sensor_name": s['sensor_name']
        })
    
    resp = {
        "sensors": sensor_list,
        "models": model_list
    }

    return resp




## To Users

@app.route("/get_all_applications", methods=['GET'])
def get_all_app():
    apps = AppInfo.query.filter().all()
    app_list = list()
    for app in apps:
        a = {
            "app_id": app.app_id,
            "app_name": app.app_name
        }
        app_list.append(a)

    return { "response": app_list }


@app.route("/get_sensor_by_app_id", methods=['POST'])
def get_sensor_by_app_id():
    req = request.get_json()
    sensor_type_id_list = AppSensorMapping.query.filter_by(app_id=req['app_id'])

    payload = {
        "app_id": req['app_id'],
        "typeid" : sensor_type_id_list[0]
    }

    response = req_sess.post(platform_endpoints['base_url'] + platform_endpoints['uri']['free_instance_by_type_id'], json=payload).json()
    return response


#To Scheduler
## app_id start time end time sensors:[ { sensor_type_id: 123, n_sensor_instance: 123  }], location: str
# ]

@app.route("/deploy")
def deploy():
    req = request.get_json()

    app = AppInfo.query.get(req['app_id'])
    if app == None:
        return {
            "status": False,
            "message": "Invalid App"
        }

    model_info = AppModelMapping.query.filter_by(app_id=req['app_id'])
    
    payload = {
        "app_id": req['app_id'],
        "start_time": req['start_time'],
        "duration": req['duration'],
        "sensors": list(),
        "location": req['location'],
        "model": model_info.model_id    #model_id is stirng
    }

    sensor_type_id_list = AppSensorMapping.query.filter_by(app_id=req['app_id'])

    for s in sensor_type_id_list:
        payload["sensors"].append(
            {
                "sensor_type_id": s.sensor_type_id,
                "n_sensor_instance": s.n_sensor_instance
            }
        )
    
    response = req_sess.post(scheduler_endpoints["base_url"] + scheduler_endpoints["uri"][""], json=payload).json()
    return response



if(__name__ == "__main__"):
    app.run(port=APP_PORT, debug=True)
