from flask import Flask, request
import requests

session = requests.Session()
app = Flask(__name__)
# myclient=pymongo.MongoClient("mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority")
# mydb=myclient["Hackathon"]
# mycollection=mydb["Request_db"]

SENSOR_PORT = 9100
MODEL_PORT = 9200
LOAD_PORT = 9300
APP_PORT = 9400
DEPLOYER_PORT = 9900
NODE_PORT = 9500
SCH_PORT = 9600


endpoint = {
    "sensor_manager": {
        "base_url": "http://localhost:"+str(SENSOR_PORT), 
        "uri": {
            "sensorinfo": "/sensorinfo",
            "getsensordata": "/getsensordata"
        }
    },
    "app_manager": {
        "base_url": "http://localhost:" + str(APP_PORT),
        "uri": {
            "get_all_models_sensos": "/get_models_sensors",
            "get_all_apps": "/get_all_applications",
            "get_sensor_by_app_id": "/get_sensor_by_app_id",
            "deploy_app": "/deploy"
        }
    },
    "load_balancer": {
        "base_url": "http://localhost:" + str(LOAD_PORT),
        "uri": {
            "get_node_id": "/get_node_id"
        }
    },
    "deployer": {
        "base_url": "http://localhost:" + str(DEPLOYER_PORT),
        "uri": {
            "send_to_deployer": "/send_to_deployer",
        }
    },
}


@app.route("/get_schedule_app", methods=["POST"])
def get_schedule_app():
    req = request.get_json()
    """
    if end_status=0:
        req={
            app_inst_id: str,
            stand_alone: bool,
            end_status: 0
        }
    else:
        req={
            app_inst_id: str,
            end_status: 1
        }

    1)if end_status==0,
        call load balancer and give stand_alone status(no use yet)
        get node id and app_inst_id to give to deployer
    2)if end_status==1,
        give empty node id and app_inst_id to deployer
    """

    deploy = {
        "app_inst_id" : req["app_inst_id"],
        "node_id":""
        }

    if req["end_status"]==0:
        load_reply = session.post(endpoint['load_balancer']['base_url'] + endpoint['load_balancer']['uri']['get_node_id'],json={'stand_alone':req['stand_alone']}).json()
        """
        load_reply={
            'node_id': str
            'message': str
        }
        """
        node_id=load_reply['node_id']
        deploy["node_id"]=node_id
        print(load_reply["message"])

    status = session.post(endpoint['deployer']['base_url'] + endpoint['deployer']['uri']['send_to_deployer'], json=deploy).json()
    """
    status={
        "status"
        "message"
    }
    """
    return status


if __name__=="__main__":
    app.run(port=NODE_PORT, debug=True)