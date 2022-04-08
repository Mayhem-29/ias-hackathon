from re import X
from flask import Flask, jsonify, redirect, request, render_template
from werkzeug.utils import secure_filename
import pymongo
import json
import os
import requests
import pickle
import zipfile
from azure.storage.fileshare import ShareFileClient
import numpy as np
import shutil
import jwt
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


req_sess = requests.Session()

app = Flask(__name__)

conn_str = 'mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority'

UPLOAD_FOLDER = os.getcwd()

client = pymongo.MongoClient(conn_str)
db = client["Hackathon"]
collection = db["ModelDB"]

app.config['SECRET_KEY'] = "dub_nation"

SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300

def read_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

constants = read_json("constants.json")

def unzip_file(file_name,source_folder):
    '''
    unzips the file to folder of same name
    '''
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(source_folder)

@app.route("/model", methods=['POST'])
def model_store_in_database():
    req = request.get_json()
    myquery = {"model_name":req["model_name"]}
    response = collection.find(myquery)

    temp_dic=[]
    for x in response:
        temp_dic.append(x)
    
    if(len(temp_dic)==0):
        temp_dic.clear()
        collection.insert_one(req)
        return "model stored"
    
    temp_dic.clear()
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
    if not os.path.exists(model_nam):
        zip_name = model_nam + ".zip"
        service = ShareFileClient.from_connection_string(conn_str="https://hackathonfilesstorage.file.core.windows.net/DefaultEndpointsProtocol=https;AccountName=hackathonfilestorage;AccountKey=gdZHKPvMvlkDnpMcxMxu2diC/bRqvjptH7qJlbx5VI/95L/p6H932ZOTZwg5kuWbyUJ6Y8TCrh3nqIlyG+YD2g==;EndpointSuffix=core.windows.net", share_name="hackathon/Model_Package", file_path=zip_name)
        with open(model_nam+".zip", "wb") as file_handle:
            data = service.download_file()
            data.readinto(file_handle)
            os.mkdir(model_nam)
        unzip_file(zip_name,os.getcwd()+"/"+model_nam)
        os.remove(zip_name)


    
    list_a = collection.find()
    pickle_file = ""
    for iter in (list_a):
        if(iter["model_name"] == model_nam):
            pickle_file = os.getcwd() + "/" + model_nam + "/" + "model.pkl"
            break
    if(pickle_file == ""):
        return jsonify({"pickle_file": "pickle file not found", "status_code":500})
    else:
        model = pickle.load(open(pickle_file, "rb"))
        prediction = str(model.predict(np.array(req["data"]).reshape(1, -1))[0])
        # shutil.rmtree(os.getcwd()+"/"+model_nam)
        return jsonify({"prediction" : prediction, "status_code" : 200})



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

# **************************** DATA SCIENTIST ********************************************************     

def model_store(data):
    model_name = data["model_name"]
    input_data = json.dumps(data["model_input"])
    no_of_inputs = len(data["model_input"])
    input_format = data["model_input_format"]
    output_format = data["model_output"]
    model_description = data["model_description"]
    request_dict = {
        "model_name": model_name,
        "no_of_inputs": no_of_inputs,
        "input_data": input_data,
        "input_format": input_format,
        "output_format": output_format,
        "model_description":model_description
    }
    response = req_sess.post(
        "http://localhost:" + str(MODEL_PORT) + "/model",
        json=request_dict).content
    response = response.decode('ascii')
    print(response)

def savefilestoazure(zip_file,model_name):
    service = ShareFileClient.from_connection_string(conn_str="https://hackathonfilesstorage.file.core.windows.net/DefaultEndpointsProtocol=https;AccountName=hackathonfilestorage;AccountKey=gdZHKPvMvlkDnpMcxMxu2diC/bRqvjptH7qJlbx5VI/95L/p6H932ZOTZwg5kuWbyUJ6Y8TCrh3nqIlyG+YD2g==;EndpointSuffix=core.windows.net", share_name="hackathon/Model_Package", file_path=model_name+".zip")
    
    with open(zip_file, "rb") as source_file:
      service.upload_file(source_file)    

# @app.route('/dataScientist_home')
# def upload_file():
#    return render_template('dataScientist.html')

@app.route("/")
@cross_origin()
def hello():
    try:
        print(request.args['jwt'])
        token = request.args['jwt']
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        # print(data)
        return render_template('dataScientist.html',
            upload_url = constants["BASE_URL"] + constants["PORT"]["MODEL_PORT"] + constants["ENDPOINTS"]["AI_MANAGER"]["dataScientist"]
        )
    except Exception as e:
        print(e)
        return redirect(constants["BASE_URL"] + constants["PORT"]["APP_PORT"] + constants["ENDPOINTS"]["APP_MANAGER"]["home"])



@app.route('/dataScientist', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      f = request.files['zipfile']
      zip_file = f
      f.save(secure_filename(f.filename))
      print(f.filename)
      try:
        with zipfile.ZipFile(f.filename) as zf:
            zf.testzip()
      except zipfile.BadZipfile:
         return False

      source_folder = os.getcwd() + "/temp"
      os.mkdir(source_folder)
      unzip_file(f.filename,source_folder)
      file_json = open(source_folder + "/config.json", "rb")
      data = json.load(file_json)
      file_json.close()
      model_name = data["model_name"]
      savefilestoazure(zip_file.filename,model_name)
      shutil.rmtree(source_folder)
      os.remove(f.filename)
      model_store(data)
      return redirect (constants["BASE_URL"] + str(constants["PORT"]["APP_PORT"]) + constants["ENDPOINTS"]["APP_MANAGER"]["home"])   

if(__name__ == "__main__"):
    app.run(port=MODEL_PORT, debug=True)
