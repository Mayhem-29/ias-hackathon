from flask import Flask, request
import requests,json

session = requests.Session()
app = Flask(__name__)

def read_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

constants = read_json("constants.json")
servers=read_json("servers.json")


@app.route("/get_schedule_app", methods=["POST"])
def get_schedule_app():
    print("Into Node manager")
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
        print("Going to Load Balancer~")
        load_reply = session.post(servers[constants["VM_MAPPING"]["LOAD"]]+constants["PORT"]["LOAD_PORT"]+constants["ENDPOINTS"]["LOAD_MANAGER"]["get_node_id"],json={'stand_alone':req['stand_alone']}).json()
        print("Back from Load Balancer~")
        """
        load_reply={
            'node_id': str
            'message': str
        }
        """
        node_id=load_reply['node_id']
        deploy["node_id"]=node_id
        print(load_reply["message"] + " and node assigned is " + str(load_reply["node_id"]))
    print("to deployer")
    status = session.post(servers[constants["VM_MAPPING"]["DEPLOYER"]]+constants["PORT"]["DEPLOYER_PORT"]+constants["ENDPOINTS"]["DEPLOYER_MANAGER"]["send_to_deployer"],json={'stand_alone':req['stand_alone']}).json()
    print("back from deployer")
    """
    status={
        "status"
        "message"
    }
    """
    print("back to scheduler")
    return status


if __name__=="__main__":
    app.run(port=constants["PORT"]["NODE_PORT"], debug=True)