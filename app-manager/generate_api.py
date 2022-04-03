import json, os

def generate_api(model_list, sensor_instances, location, folder):

    try:
        constant_file = open("constants.json", "r")
        constants = json.loads(constant_file.read())
        constant_file.close()
        SENSOR_API = constants["BASE_URL"] + constants["PORT"]["APP_PORT"] + constants["ENDPOINTS"]["APP_MANAGER"]["get_sensor_data"]
        MODEL_API = constants["BASE_URL"] + constants["PORT"]["APP_PORT"] + constants["ENDPOINTS"]["APP_MANAGER"]["get_model_predict"]

        read_sensor_payload = '{ "sensor_instance_id": SENSOR_INSTANCE_LIST[idx] }'
        read_model_payload = '{ "model_name": MODEL_LIST[idx], "data": data }'
        
        function_code = """
import requests

LOCATION = "{loc}"
SENSOR_API = "{SENSOR_API}"
MODEL_API = "{MODEL_API}"

SENSOR_INSTANCE_LIST = {sensor_ins_id}
MODEL_LIST = {model_list}

def get_sensor_data(idx):
    payload = {sensor_payload}
    resp = requests.post(SENSOR_API, json=payload).json()
    return resp


def use_model(idx, data):
    payload = {model_payload}
    resp = requests.post(MODEL_API, json=payload).json()
    return resp


def pre_process(data):
    return data


def post_process(data):
    return data

        """.format(
            loc=location,
            sensor_ins_id=sensor_instances,
            model_list=model_list,
            SENSOR_API=SENSOR_API,
            MODEL_API=MODEL_API,
            sensor_payload=read_sensor_payload,
            model_payload = read_model_payload
        )

        if not os.path.exists('out'):
            os.makedirs('out')

        api_file = open("out/API.py", "w+")
        api_file.write(function_code)
        api_file.close()

        return True
    except:
        return False