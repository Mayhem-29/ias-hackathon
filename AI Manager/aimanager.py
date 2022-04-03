from flask import Flask
from flask import session
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

from model_server import Model_db

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"

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

SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300


@app.route("/list_of_models", methods=['GET'])
def get_list():
    list_a = Model_db.query.filter().all()
    model_list = list()
    for j in range(len(list_a)):
        model_list.append(list_a[j].model_name)
    return jsonify({"model_list": model_list, "status_code": 200})


@app.route("/get_pickle", methods=['POST'])
def get_pkl():  
    req = request.get_json()
    model_nam=req.get('model_name')
    list_a = Model_db.query.filter().all()
    pickle_file = ""
    for j in range(len(list_a)):
        if(list_a[j].model_name==model_nam):
            pickle_file = list_a[j].pkl_url
            break
    if(pickle_file==""):
        return jsonify({"pickle_file": "pickle file not found"})
    else:
        return jsonify({"pickle_file": pickle_file})


if(__name__ == "__main__"):
    app.run(port=MODEL_PORT, debug = True)