import json, os

def generate_api(model_list, sensor_instances, controller_instances, location, folder, app_name):
    print(folder)
    try:
        constant_file = open("constants.json", "r")
        constants = json.loads(constant_file.read())
        constant_file.close()

        servers_file = open("servers.json", "r")
        servers = json.loads(servers_file.read())
        servers_file.close()

        SENSOR_API = servers[constants["VM_MAPPING"]["APP"]] + constants["PORT"]["APP_PORT"] + constants["ENDPOINTS"]["APP_MANAGER"]["get_sensor_data"]
        MODEL_API = servers[constants["VM_MAPPING"]["APP"]] + constants["PORT"]["APP_PORT"] + constants["ENDPOINTS"]["APP_MANAGER"]["get_model_predict"]
        CONTROLLER_API = servers[constants["VM_MAPPING"]["APP"]] + constants["PORT"]["APP_PORT"] + constants["ENDPOINTS"]["APP_MANAGER"]["send_controller_message"]

        read_sensor_payload = '{ "sensor_instance_id": SENSOR_INSTANCE_LIST[idx] }'
        read_model_payload = '{ "model_name": MODEL_LIST[idx], "data": data }'
        post_controller_payload = '{ "controller_instance_id": CONTROLLER_INSTANCE_LIST[idx], "data": data }'
        
        function_code = """
import requests

LOCATION = "{loc}"
SENSOR_API = "{SENSOR_API}"
MODEL_API = "{MODEL_API}"
CONTROLLER_API = "{CONTROLLER_API}"

SENSOR_INSTANCE_LIST = {sensor_ins_ids}
MODEL_LIST = {model_list}
CONTROLLER_INSTANCE_LIST = {controller_ins_ids}

def get_sensor_data(idx):
    payload = {sensor_payload}
    resp = requests.post(SENSOR_API, json=payload).json()
    return resp["message"]


def post_controller_message(idx, data):
    payload = {controller_payload}
    resp = requests.post(CONTROLLER_API, json=payload).json()
    return resp["message"]


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
            sensor_ins_ids=sensor_instances,
            controller_ins_ids=controller_instances,
            model_list=model_list,
            SENSOR_API=SENSOR_API,
            MODEL_API=MODEL_API,
            CONTROLLER_API=CONTROLLER_API,
            sensor_payload=read_sensor_payload,
            model_payload = read_model_payload,
            controller_payload = post_controller_payload
        )

        path = folder + "/" + app_name
        print(path)
        api_file = open(path + "/api.py", "w+")
        api_file.write(function_code)
        api_file.close()
        print("OK2")

        return True
    except Exception as e:
        print("exception in genrate_api", e)
        return False