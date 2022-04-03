
def generate_api(model_list, sensor_instances, location, folder):

    try:
        code = """
import json
import requests

constant_file = open("../constants.josn", "r")
constants = json.loads(constant_file)

LOCATION = "{loc}"
SENSOR_API = constants["BASE_URL"] + constants["POST"]["APP_PORT"] + constants["ENDPOINTS"]["APP_MANAGER"]["get_sensor_data"]
MODEL_API = constants["BASE_URL"] + constants["POST"]["APP_PORT"] + constants["ENDPOINTS"]["APP_MANAGER"]["get_model_predict"]

SENSOR_INSTANCE_LIST = [{sensor_ins_id}]
MODEL_LIST = [{model_list}]

def get_sensor_data(idx):
    payload = {
        "sensor_instance_id": SENSOR_INSTANCE_LIST[idx]
    }
    resp = requests.post(SENSOR_API, json=payload).json()
    return resp


def use_model(idx, data):
    payload = {
        "model_name": MODEL_LIST[idx],
        "data": data
    }
    resp = requests.post(MODEL_API, json=payload).json()
    return resp


def pre_process(data):
    return data


def post_process(data):
    return data

    """.format(
        loc=location,
        sensor_ins_id=sensor_instances,
        model_list=model_list
    )

        api_file = open(folder + "/api.py", "w")
        api_file.write(code)
        api_file.close()

        return True
    except:
        return False