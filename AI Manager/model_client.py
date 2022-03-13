import requests
from getpass import getpass
req_sess = requests.Session()

def model_store():
    model_name = "digit_pred"
    input_format = "image"
    output_format = "int"
    # url="https://drive.google.com/file/d/171qJj28QsBKv4JUO2sXnyDGVqOFd3v_u/view?usp=sharing"
    url = "/Users/ashishrai/Documents/Ashish/IIITH/Sem2-courses/Courses/IAS/Project/code/hack1/AI Manager/model.pkl"
    request_dict = {
        "model_name": model_name,
        "input_format": input_format,
        "output_format": output_format,
        "pkl_url":url
    }

    response = req_sess.post(
        "http://localhost:8000/" + "/model",
        json=request_dict).content
    print(response.decode('ascii'))

def getmodellist():
     response = req_sess.get("http://localhost:8000/" + "/list_of_models").json()
     if(response["status_code"] == 501):
        print(response["error"])
     print(response)

def getpickle():
    model_name = "digit_pred"
    request_dict = {
        "model_name": model_name
    }
    response = req_sess.post(
        "http://localhost:8000/" + "/get_pickle",
        json=request_dict).json()
    print(response)    

model_store()
