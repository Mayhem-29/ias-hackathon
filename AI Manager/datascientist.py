from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
import os
import requests
import json
req_sess = requests.Session()

app = Flask(__name__)

DATA_SCIENTIST_PORT = 9450
SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300

base_url = "http://localhost:" + str(DATA_SCIENTIST_PORT) 

def model_store(f,f1):
    file_json = open(f1.filename)
    data = json.load(file_json)
    file_json.close()
    model_name = data["model_name"]
    input_data = json.dumps(data["model_input"])
    no_of_inputs = len(data["model_input"])
    input_format = data["model_input_format"]
    output_format = data["model_output"]
    url = os.getcwd() + "/"+ f.filename
    model_description = data["model_description"]
    request_dict = {
        "model_name": model_name,
        "no_of_inputs": no_of_inputs,
        "input_data": input_data,
        "input_format": input_format,
        "output_format": output_format,
        "pkl_url":url,
        "model_description":model_description
    }
   #  api_test = {
   #     "model_name": model_name
   #  }
    response = req_sess.post(
        "http://localhost:" + str(MODEL_PORT) + "/model",
        json=request_dict).content
    response = response.decode('ascii')
    message = ""
    if(response == "model already exists"):
       message = "Model name already exists. Again upload files with unique model name"
    else:
      message = "Files uploaded"
    return message
   #  response = req_sess.get("http://localhost:" + str(MODEL_PORT) + "/list_of_models").content
   #  print(response)
   #  response = req_sess.post(
   #      "http://localhost:" + str(MODEL_PORT) + "/get_pickle_location",
   #      json=api_test).content
   #  print(response)
    

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      f = request.files['picklefile']
      f.save(secure_filename(f.filename))
      f1 = request.files['configfile']
      f1.save(secure_filename(f1.filename))      
      return model_store(f,f1)

if __name__ == '__main__':
    app.run(port=DATA_SCIENTIST_PORT, debug=True)