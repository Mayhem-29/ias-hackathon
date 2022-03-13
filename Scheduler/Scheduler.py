from flask import Flask,json, request
import json, requests
from threading import Thread
from datetime import datetime
import heapq

app = Flask(__name__)
sess = requests.Session()

SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300
APP_PORT = 9400
DEPLOYER_PORT = 9500
NODE_PORT = 9500
SCH_PORT = 9600


DeployerURL="http://localhost:8080"

uri={
    "userInput":"/get_schedule_app"
}

scheduler_endpoints = {
    "base_url": "http://localhost:" + str(DEPLOYER_PORT),
    "uri": {
        "userInput": "/get_schedule_app"
    }
}




Scheduler_queue=[]

@app.route('/sendInfo',methods=['POST'])
def getUserInput():
    # data = json.loads(request.data)
    response=request.get_json()
    data={}
    result={"status":"false"}
    
    data["start_time"]=response["start_time"]
    data["end_time"]=response["end_time"]
    data["app_id"]=response["app_id"]
    data["location"]=response["location"]
    data["sensors"]=response["sensors"]
    data["app_path"]=response["app_path"]
    heapq.heappush(Scheduler_queue,(data["start_time"],data["end_time"],data["app_id"],data))
    result["status"]="true"
    
    return json.dumps(result)



def deployerApp(appInfo):
    # print("abcd")
    deployer_obj={}
    deployer_obj["app_id"]=appInfo["app_id"]
    deployer_obj["end_time"]=appInfo["end_time"]
    deployer_obj["location"]=appInfo["location"]
    deployer_obj["sensors"]=appInfo["sensors"]
    deployer_obj["app_path"]=appInfo["app_path"]
    # deployer_json=json.dumps(deployer_obj)
    # response=sess.post(url=DeployerURL+uri["userInput"],data=deployer_json).json()
    response=sess.post(url= scheduler_endpoints["base_url"] +scheduler_endpoints["uri"]["userInput"],json = deployer_obj).json()
    if response["status"]=="true":
        print("Application ID "+appInfo["app_id"]+" deployed successfully")
    else:
        print("Application ID "+appInfo["app_id"]+" failed to deploy")


def scheduling_function():
    #print("Cgfdg")
    while(True):
        if Scheduler_queue:
            while str(datetime.now()).rsplit(':',1)[0]<Scheduler_queue[0][0]:
                pass
            appInfo = heapq.heappop(Scheduler_queue)[3]
            deployerApp(appInfo)


if __name__=="__main__":
    thread=Thread(target=scheduling_function)
    thread.start()

    app.run(port=SCH_PORT)

    thread.join()