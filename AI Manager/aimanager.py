from re import X
from flask import Flask
from flask import session
from flask import jsonify
from flask import request
from flask_mongoalchemy import MongoAlchemy
import pymongo
import os
import pickle

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

    temp_dic={}
    for x in response:
        temp_dic.add(x)
    
    if(len(temp_dic)==0):
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


@app.route("/get_prediction", methods=['POST'])
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
        input_preprocessed = os.system('python preprocessor.py ', req.get('input'))
        model = pickle.load(open(pickle_file, "rb"))
        prediction = str(model.predict(input_preprocessed))
        output = os.system('python postprocessor.py' + prediction)
        return jsonify({"prediction" : output, "status_code" : 200})



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

@app.route("/all_model_details", methods=['GET'])
def all_model_details():
    model_info = {}
    list_a = collection.find()
    for iter in list_a:
        model_info[iter["model_name"]] = {"no_of_inputs":iter["no_of_inputs"], "input_data":iter["input_data"], "input_format":iter["input_format"], "output_format":iter["output_format"], "model_description":iter["model_description"]}
    return jsonify({"model_info": model_info, "status_code": 200})

if(__name__ == "__main__"):
    app.run(port=MODEL_PORT, debug=True)
