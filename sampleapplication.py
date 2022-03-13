import sys
from flask import Flask, request
import requests
import json
import pickle
import numpy as np

sess = requests.Session()

PLATFORM_PORT = 9300

platform_endpoints = {
    "base_url": "http://localhost:" + str(PLATFORM_PORT),
    "uri": {
        "get_sensor_info": "/get_sensor_info",
        "get_model_info": "/get_model_info",
        "free_instance_by_type_id": "/free_instance_by_type_id",
        "predict_model": "/predict_model"
    }
}

def run_app():
    sensor_data = sys.argv[1]
    model_data = sys.argv[2]

    sensor_file = open(sensor_data)
    sensor_req = json.load(sensor_file)

    model_file=open(model_data)
    model_req = json.load(model_file)

    payload = {
        "model_name" : model_req['model_name'] ,
        "tid" : sensor_req['type_id'][0] , 
        "location" : sensor_req['location']
    }

    prediction = sess.post(platform_endpoints["base_url"] + platform_endpoints["uri"]["predict_model"], json = payload).json()

    return prediction


if __name__ == "__main__":
    while True:
        optn = input("Enter 1 to run app, 2 to exit: ")
        if optn=="2":
            break
        else:
            print(run_app())