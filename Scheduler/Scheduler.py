from flask import Flask,json,request
import pymongo
import json, requests
from threading import Thread
from datetime import datetime,date,timedelta
import math
import heapq

app = Flask(__name__)
myclient=pymongo.MongoClient("mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority")
mydb=myclient["Hackathon"]
mycollection=mydb["Request_db"]
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

"""
Database for requests
"""

Scheduler_queue=[]
Termination_queue=[]

@app.route('/sendInfo',methods=['POST'])
def getUserInput():
    response=request.get_json()
    result={"status":"false"}
    """
    1)take this response object and pass it to request db as it is
    2)get the request id 
    3)take start time, end time, request id
      andadd to first priority queue 
    """
    #1
    doc=mycollection.insert_one(response)
   
    #2
    request_id=doc.inserted_id
    #3
    heapq.heappush(Scheduler_queue,(response["start_time"],response["end_time"],request_id))
    result["status"]="true"
    
    return json.dumps(result)



def deployerApp(appInfo):
    deployer_obj={}
    deployer_obj["request_id"]=str(appInfo[2])
    deployer_obj["end_status"]=0

    # print("72...sending to deployer to deploy")
    response=sess.post(url= scheduler_endpoints["base_url"] +scheduler_endpoints["uri"]["userInput"],json = deployer_obj).json()

    """
    1)response status = true
        1.1)calculate the end time
        1.2)take end time, req id
            and add to the second priority queue
    2)remove the corresponding req id entry from db
    """

    #1
    if response["status"]=="true":
        #1.1
        duration=float(appInfo[1])
        days_num=duration/int(24)
        rem=duration%24
        hours=math.floor(rem)
        min=math.floor((rem-hours)*60)
        date_time = datetime.strptime(appInfo[0] + ":00", '%Y-%m-%d %H:%M:%S')
        end_date=date_time + timedelta(days=days_num)
        end_time=str(end_date)+" "+str(hours)+":"+str(min)
        end_time = end_time.rsplit(':',2)[0]
        #this end_time is  String
        #1.2
        heapq.heappush(Termination_queue,(end_time,deployer_obj["request_id"]))
    
    #2
    # print("99")
    mycollection.delete_one({"_id": appInfo[2]})
   


def scheduling_function():
    
    while(True):
        if Scheduler_queue:
            while str(datetime.now()).rsplit(':',1)[0]<Scheduler_queue[0][0]:
                pass
            appInfo = heapq.heappop(Scheduler_queue)
            deployerApp(appInfo)

def termination_function():
    
    while(True):
        if Termination_queue:
            # print("118 --- ",Termination_queue[0][0])
            while str(datetime.now()).rsplit(':',1)[0]<Termination_queue[0][0]:
                pass
            # print("121 termination function ",str(datetime.now()).rsplit(':',1)[0])
            kill_id = heapq.heappop(Termination_queue)[1]
            deployer_obj={}
            deployer_obj["request_id"]=kill_id
            deployer_obj["end_status"]=1
            response=sess.post(url= scheduler_endpoints["base_url"] +scheduler_endpoints["uri"]["userInput"],json = deployer_obj).json()
            # print(response)

if __name__=="__main__":
    """
    1)thread1 = to continuously check if start time of any app in scheduling queue has come
    2)thread2 = to check continuously if end time of any deployed app has been reached
    """
    thread1=Thread(target=scheduling_function)
    thread2=Thread(target=termination_function)
    thread1.start()
    thread2.start()

    app.run(port=SCH_PORT)

    thread1.join()
    thread2.join()