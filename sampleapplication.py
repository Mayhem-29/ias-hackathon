import sys
from flask import Flask, request
import requests
import json
import pickle
import numpy as np

sess = requests.Session()


if __name__ == "__main__":
    sensor_data = sys.argv[1]
    model_data = sys.argv[2]
    sensor_file = open(sensor_data)
    sensor_req = json.load(sensor_file)
    model_file=open(model_data)
    model_req = json.load(model_file)
    response_model = sess.post('http://localhost:8070/get_pickle', json = model_req).json()
    sensor_string = str(sensor_req["type_id"][0]) + "," + str(sensor_req["location"])
    response_sensor = sess.get("http://localhost:8000/getsensordata/" + sensor_string).json()
    model = pickle.load(open(response_model["pickle_file"], "rb"))
    prediction = str(model.predict(np.array(response_sensor["data"]).reshape(1,-1))[0])
    ans = {
        "output" : prediction ,
        "status_code" : 200
    }
    print (ans)