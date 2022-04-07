from asyncio import subprocess
from concurrent.futures import thread
from flask import Flask, request
import requests
import os
import json
from queue import PriorityQueue
from threading import Thread
from datetime import datetime
from azure.storage.fileshare import ShareFileClient
from paramiko import SSHClient, AutoAddPolicy
import pymongo
from psutil import process_iter
from signal import SIGTERM
from flask_cors import CORS, cross_origin
from subprocess import Popen
from bson import ObjectId
import time
import threading
import generate_docker_file as gdf



session = requests.Session()
app = Flask(__name__)
cors = CORS(app)

SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300
APP_PORT = 9400
DEPLOYER_PORT = 9900
NODE_PORT = 9700
SCH_PORT = 9600
CONNECTION_STR = "https://hackathonfilestorage.file.core.windows.net/DefaultEndpointsProtocol=https;AccountName=hackathonfilestorage;AccountKey=gdZHKPvMvlkDnpMcxMxu2diC/bRqvjptH7qJlbx5VI/95L/p6H932ZOTZwg5kuWbyUJ6Y8TCrh3nqIlyG+YD2g==;EndpointSuffix=core.windows.net"

session = requests.Session()
app = Flask(__name__)
client = SSHClient()
myclient=pymongo.MongoClient("mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority")
mydb=myclient["Hackathon"]
nodedb=mydb["Node_db"]
# appdb = mydb["app_inst_db"]
appdb = mydb["AppInstance"]

base_url = "http://localhost:8080"

# ports = 9751
port_dict = dict()
ports = {
    2000 : "False",
    2001 : "False",
    2002 : "False",
    2003 : "False",
    2004 : "False",
    2005 : "False"
}

@app.route("/")
@cross_origin()
def hello():
    return ""

@app.route("/send_to_deployer", methods=["POST"])
def send_to_deployer():
    print("Starting Deployment")
    req = request.get_json()
    
    node_id = req["node_id"]
    app_inst_id = req["app_inst_id"]
    app_path = ""
    print("app instance : ", app_inst_id)

    """
    1) if node_id==""
        this means that the app is already running and it has to be killed
        1.1)goto appInsDB and fetch node_id
        1.2)delete that row from appInst db
        1.3)corresponding to the node_id, get the pid from dict and kill the process
        1.4)delete the appInstId from NodeDb list of inst of that node

    2) otherwise run the app at the given node

    """

    #1
    if node_id == "":
        if port_dict[app_inst_id] == None:
            print("port dictionary empty!")
            status = {
                "status":"true",
                "message":"Port Dictionary empty for given app instance id!"
            }
            return status

        kill_port = port_dict[app_inst_id]
        # pid = port_dict[app_inst_id][1]
        

        for x in appdb.find():
            if str(x["_id"]) == app_inst_id:
                node_id = x["node_id"]
                print(x)
                print(x["node_id"])
                appdb.delete_one(x)
                print("deletion done in appdb")
                break
        
        temp = nodedb.update_one({ "_id": ObjectId(node_id) },
                            { "$pull": { 'list_of_app_inst': app_inst_id } }
                        )
                

        # kill_port = port_dict[app_inst_id][0]
        # pid = port_dict[app_inst_id][1]


        # cmd = "taskkill /im" + str(pid)
        # cmd = "sudo pkill -9 -P" + str(pid)
        # os.system(cmd)
        # kill_port = port_dict[app_inst_id]
        # for proc in process_iter():
        #     for conns in proc.connections(kind='inet'):
        #         if conns.laddr.port == kill_port:
        #             proc.send_signal(SIGTERM)
        print("kill_time")
        os.system(f"sudo docker exec -it $(sudo docker ps -q --filter ancestor={app_inst_id}) kill 1")
        os.system(f"sudo docker image remove -f {app_inst_id})")
        ports[kill_port] = "False"
        # port_dict[app_inst_id] = None
        del port_dict[app_inst_id]

        status = {
            "status":"true",
            "message":"Process Killed!"
        }
        
    else:
        curr_port = None
        for curr_port in ports.keys():
            if ports[curr_port] == "False":
                key = curr_port
                break
        if key == None:
            return {"status" : "false", "message" : "No Port Available"}
        
        port_dict[app_inst_id] = key
        print("app path: " , app_path)

        temp = nodedb.update_one({ "_id": ObjectId(node_id) },
                    { "$push": { 'list_of_app_inst': app_inst_id}}
                    )
        
        for x in appdb.find():
            if str(x["_id"]) == app_inst_id:
                appdb.update_one({"_id" : ObjectId(app_inst_id)}, {"$set" : {"node_id" : node_id}})
                app_path = x["docker_image"]
                break
        
        # k = None
        # for k in ports.keys():
        #     if ports[k] == "False":
        #         key = k
        #         break
        # if key == None:
        #     return {"status" : "false", "message" : "No Port Available"}
        # port_dict[app_inst_id] = []
        # port_dict[app_inst_id].append(key)
        # print("app path: " , app_path)

        gdf.generate_dockerfile(curr_port, app_path)

        os.system(f"sudo docker build -t {app_inst_id}:latest {app_path}")
        os.system(f"sudo docker run --net=host -it -d -p {curr_port}:{curr_port} {app_inst_id}")

        print("app running at port {}".format(curr_port))
        
        # port_dict[app_inst_id].append(p.pid)
        # port_dict[app_inst_id].append(55402)
        # os.system(command)
        # ports = ports + 1
        
        ports[curr_port] = "True"
        status = {
            "status":"true",
            "message":"Deployed!"
        }
        print(curr_port)

    print (port_dict)
    return status

if __name__=="__main__":
    app.run(port=DEPLOYER_PORT, debug=True) 