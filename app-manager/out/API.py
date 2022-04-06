
import requests

LOCATION = "bakul"
SENSOR_API = "http://localhost:9400/get_sensor_data"
MODEL_API = "http://localhost:9400/get_model_predict"

SENSOR_INSTANCE_LIST = <Response 63 bytes [200 OK]>
MODEL_LIST = ['digit_pred']

def get_sensor_data(idx):
    payload = { "sensor_instance_id": SENSOR_INSTANCE_LIST[idx] }
    resp = requests.post(SENSOR_API, json=payload).json()
    return resp


def use_model(idx, data):
    payload = { "model_name": MODEL_LIST[idx], "data": data }
    resp = requests.post(MODEL_API, json=payload).json()
    return resp


def pre_process(data):
    return data


def post_process(data):
    return data

        