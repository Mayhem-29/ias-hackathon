from flask import Flask
from flask import session
from flask import jsonify
from flask import request
from flask_mongoalchemy import MongoAlchemy
import pymongo

app = Flask(__name__)

conn_str = 'mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority'

client = pymongo.MongoClient(conn_str)
db = client["Hackathon"]
collection = db["ModelDB"]


SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300


@app.route("/model", methods=['POST'])
def model_store():
    req = request.get_json()
    myquery = {"model_name":req["model_name"]}
    response = collection.find(myquery)
    if(response == None):
        collection.insert_one(req)
        return "model stored"
    return "model already exists"

@app.route("/list_of_models", methods=['GET'])
def get_list():
    list_a = collection.find()
    model_list = list()
    for iter in list_a:
        model_list.append(iter["model_name"])
    return jsonify({"model_list": model_list, "status_code": 200})


@app.route("/get_pickle_location", methods=['POST'])
def get_pkl():
    req = request.get_json()
    model_nam = req.get('model_name')
    list_a = collection.find()
    pickle_file = ""
    for iter in (list_a):
        if(iter["model_name"] == model_nam):
            pickle_file = iter["pkl_url"]
            break
    if(pickle_file == ""):
        return jsonify({"pickle_file": "pickle file not found", "status_code":500})
    else:
        return jsonify({"pickle_file": pickle_file, "status_code":200})

@app.route("/model_details", methods=['POST'])
def model_details():
    req = request.get_json()
    model_nam = req.get('model_name')
    model_info = {}
    list_a = collection.find()
    for iter in list_a:
        if(iter["model_name"] == model_nam):
            model_info["no_of_inputs"] = iter["no_of_inputs"]
            model_info["input_data"] = iter["input_data"]
            model_info["input_format"] = iter["input_format"]
            model_info["output_format"] = iter["output_format"]
            model_info["model_description"] = iter["model_description"]
    if(model_info == ""):
        return jsonify({"status_code": 500})
    else:
        return jsonify({"model_info": model_info, "status_code": 200})


if(__name__ == "__main__"):
    app.run(port=MODEL_PORT, debug=True)
