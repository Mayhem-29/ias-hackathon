from flask import Flask, redirect
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
import os
import requests
import json
import zipfile
import shutil
from azure.storage.fileshare import ShareFileClient
from azure.storage.fileshare import ShareDirectoryClient
import os
from azure.identity import DefaultAzureCredential
from flask_cors import CORS, cross_origin



req_sess = requests.Session()

x = 1

UPLOAD_FOLDER = os.getcwd()

app = Flask(__name__)
cors = CORS(app)

DATA_SCIENTIST_PORT = 9450
SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300

base_url = "http://localhost:" + str(DATA_SCIENTIST_PORT) 

def allowed_file(filename):
    '''
    checks if file is zip
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(["zip"])


def unzip_file(file_name,source_folder):
    '''
    unzips the file to folder of same name
    '''
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(source_folder)
        
def validate_zip(file_name):
    '''
    validates zip file
    '''
    try:
        with zipfile.ZipFile(file_name) as zf:
            zf.testzip()
    except zipfile.BadZipfile:
        return False

    unzip_file(file_name)
    folder_name = os.path.splitext(file_name)[0]
    config_json = json.load(folder_name + "/config.json")
    app_name = config_json["model_name"]

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
    file_json = open("modeldata.json")
    model_data = json.load(file_json)
    file_json.close()
    
def savefilestoazure(zip_file,model_name):
    service = ShareFileClient.from_connection_string(conn_str="https://hackathonfilesstorage.file.core.windows.net/DefaultEndpointsProtocol=https;AccountName=hackathonfilestorage;AccountKey=gdZHKPvMvlkDnpMcxMxu2diC/bRqvjptH7qJlbx5VI/95L/p6H932ZOTZwg5kuWbyUJ6Y8TCrh3nqIlyG+YD2g==;EndpointSuffix=core.windows.net", share_name="hackathon/Model_Package", file_path=model_name+".zip")
    
    with open(zip_file, "rb") as source_file:
      service.upload_file(source_file)



@app.route("/")
@cross_origin()
def hello():
    return ""

@app.route('/upload')
def upload_file():
   return render_template('dataScientist.html')

@app.route('/dataScientist', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      f = request.files['zipfile']
      zip_file = f
      f.save(secure_filename(f.filename))

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
      print("File Uploaded")
      return redirect ('/upload')

if __name__ == '__main__':
    app.run(port=DATA_SCIENTIST_PORT, debug=True)