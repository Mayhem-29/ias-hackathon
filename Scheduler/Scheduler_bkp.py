# import imp
from flask import Flask,json, request
from queue import PriorityQueue
import json, requests
from threading import Thread
from datetime import datetime

app = Flask(__name__)
sess = requests.Session()

DeployerURL="http://127.0.0.1:8080"

uri={
    "userInput":"/get_schedule_app"
}

Scheduler_queue=PriorityQueue()

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
    Scheduler_queue.put(data)
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
    response=sess.post(url=DeployerURL+uri["userInput"],json = deployer_obj).json()
    if response["status"]=="true":
        print("Application ID "+appInfo["app_id"]+" deployed successfully")
    else:
        print("Application ID "+appInfo["app_id"]+" failed to deploy")


def scheduling_function():
    #print("Cgfdg")
    while(True):
        if not Scheduler_queue.empty():
            appInfo=Scheduler_queue.get()
            while str(datetime.now()).rsplit(':',1)[0]<appInfo["start_time"]:
                pass
            deployerApp(appInfo)


if __name__=="__main__":
    thread=Thread(target=scheduling_function)
    thread.start()

    app.run(port=1337)

    thread.join()
    

