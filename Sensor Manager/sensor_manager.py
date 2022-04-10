from flask import Flask,render_template,request,redirect
import random
import json

import time
import threading
import pymongo
# from topics import * 
from flask_cors import CORS, cross_origin
import jwt

from init_sensor import *


def read_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

constants = read_json("constants.json")


############################################## List of APIs #######################################################

# @app.route("/")
# @app.route("/is_sensor_manager_alive")
# @app.route('/appdev_insert_type/<string:sensor_type>/<string:output_type>')
# @app.route('/list_of_sensortypes')
# @app.route('/install_sensorins', methods=["POST"])
# @app.route('/delete_sensorins', methods=["POST"])
# @app.route('/newsensorinfo')
# @app.route('/list_sensor_info_by_loc')
# @app.route('/newsensorinfo_ap')


##################################################################################################################

    


# **************************************** Pymongo *******************************************************

cluster = pymongo.MongoClient('mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority')
db = cluster["Hackathon"]
type_info = db["sensor_type_info"]
ins_info = db["sensor_instance_info"]






# ***************************************** Kafka *********************************************************

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.consumer import KafkaConsumer
from kafka import KafkaProducer

IP_ADDR = constants["KAFKA_HOST_ADDR"]

def serialize(msg):
        return json.dumps(msg).encode('utf-8')


producer = KafkaProducer(
    bootstrap_servers = [IP_ADDR],
    value_serializer = serialize
)

client = KafkaAdminClient(
    bootstrap_servers = [IP_ADDR]
)

def create_topic(topic_name):

    topics = list()
    try:
        topics.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
        client.create_topics(topics)
        print("Topic created sucessfully")
        return True
    except:
        print("Something went wrong")
        return False

def data_producer(topic,data_type,fg):
    
    if(fg==1):
        create_topic(topic)
    
    producer = KafkaProducer(
        bootstrap_servers = [IP_ADDR],

        value_serializer = serialize
    )
    if(data_type=="int"):
        while True:
            msg = random.randint(10,10000)
            producer.send(topic,msg)
            # print("Producer : ", msg)
            # time.sleep(1)

    elif(data_type == "float"):
        while True:
            msg = int(random.random()*100)/100
            producer.send(topic,msg)
            # print("Producer : ", msg)
            # time.sleep(1)

    elif(data_type=='array'):
        while True:
            f=open("data.json")
            data = json.load(f)
            i = random.randint(0,4)
            msg=data[str(i)]
            producer.send(topic,msg)
            # print("Producer : ", msg)
            # time.sleep(1)



admin_client = KafkaAdminClient(
    bootstrap_servers = [IP_ADDR]
)     


# ********************************************** INIT Kafka  *******************************************************






############################################################################################################


app = Flask(__name__)
cors = CORS(app)
# app.config['SECRET_KEY'] = "sensor_manager"
app.config['SECRET_KEY'] = "dub_nation"
def generateint():
    return random.randint(10,10000)

def generatefloat():
    return int(random.random()*100)/100



@app.route("/")
@cross_origin()
def home():
    try:
        print(request.args['jwt'])
        token = request.args['jwt']
        print("HI")
        # data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        # print(data)
        return render_template("installsensor.html",
            home=constants["BASE_URL"] + str(constants["PORT"]["APP_PORT"]) + constants["ENDPOINTS"]["APP_MANAGER"]["home"]
        )
    except:
        return redirect(constants["BASE_URL"] + constants["PORT"]["APP_PORT"] + constants["ENDPOINTS"]["APP_MANAGER"]["home"])
    

@app.route("/is_sensor_manager_alive")
def is_sensor_manager_alive():
    '''
    Check for sensor Alive Status
    '''
    
    
    # print(list_topics())
    return  {"status":"yes"}



@app.route('/appdev_insert_type/<string:sensor_type>/<string:output_type>')
def appdev_insert_type(sensor_type,output_type):
    '''
    Add Sensor type by Application Manager
    '''
    
    
    
    q1 = { "sensor_type": sensor_type }

    # mdl = type_info.query.get(sensor_type)
    mdl = type_info.find(q1) 

    alldata=[]
    
    for i in mdl:
        alldata.append(i)


    if(len(alldata)==0):
        #model = type_info(sensor_type=sensor_type,output_type=output_type)
        type_info.insert_one({"sensor_type":sensor_type, "output_type":output_type})
    ans = {"response":"ok"}
    return ans  

@app.route('/list_of_sensortypes')
def list_of_sensortypes():
    '''
    Lists Sensor types available on Platform
    '''
    
    

    mdl=type_info.find()
    ans=[]
    for x in mdl:
        ans.append(x["sensor_type"])
    
    return {"response":ans}
    

@app.route('/install_sensorins', methods=["POST"])
def install_sensorins():
    '''
    Add Sensor Instance by Platform Admin
    '''
 
    if request.method=="POST":

        sensor_type=request.form.get("sensor_type")
        location=request.form.get("location")
        sensor_ip = request.form.get("sensor_ip")
        sensor_port = request.form.get("sensor_port")
    
        # resp=request.get_json()
        # resp = resp['sensor_data'][0]
        # print(resp)
        # sensor_type= resp["sensor_type"]
        # location=resp["location"]
        # sensor_ip=resp["sensor_ip"]
        # sensor_port=resp["sensor_port"]
            
        q1={"sensor_type": sensor_type}
        mdl=type_info.find(q1)
        flag=0
        for x in mdl:
            if(x["sensor_type"]==sensor_type):
                flag=1
                break
        if(flag==1):
            ins_info.insert_one({"sensor_type": sensor_type , "location" : location, "sensor_ip" : sensor_ip, "sensor_port":sensor_port  })
            # ins_info.insert_one(resp)

            all = ins_info.find()
            alldata   = []

            for i in all:
                alldata.append(i)
            d_type = ""
            q1 = {"sensor_type":sensor_type}
            ab = type_info.find(q1)

            for x in ab:
                d_type = x["output_type"]

            print(d_type)
            ins_id = str(alldata[len(alldata)-1]["_id"])
            print(ins_id)

            # js = {"topic":ins_id, "output_type":d_type}
            # post_to_producer("comm_sensor_metadata", js)
            fg=1
            t = threading.Thread(target=data_producer, args=[ins_id,d_type,fg])
            t.start()
            
             
    return redirect("/")
     
    # redirect('/installsensor')            



@app.route('/delete_sensorins', methods=["POST"])
def delete_sensorins():
    '''
    Delete Sensor Instance by Platform Admin
    '''
    
    if request.method=="POST":
        sensor_type=request.form.get("sensor_type")
        location=request.form.get("location")
        
        ins_info.delete_one({"sensor_type":sensor_type,"location":location})
    return redirect("/")
            

@app.route('/newsensorinfo')
def newsensorinfo():
    '''
    {
        "response":[
                        {
                            "location":"hyd",
                            "sensors": [
                                            {
                                                "instances":["1234","2468"],
                                                "sensor_type":"temp"   
                                            },
                                            {
                                                "instances":["4321","6812","6789","1574"],
                                                "sensor_type":"camera"
                                            }
                                        ]
                        }
                    ]
    }
    '''

    all = ins_info.find()
    alldata   = []

    for i in all:
        alldata.append(i)


    stloc = set()
    stsen = set()


    for x in alldata:
        stloc.add(x["location"])
        stsen.add(x["sensor_type"])

    stloc = list(stloc)
    stsen = list(stsen)
    ans = {}
    loc_info=[]

    for loc in stloc:
        diction=dict()
        diction["location"]=loc
        diction["sensors"]=[]
        for x in alldata:
            if(x["location"]!=loc):
                continue
            else:
                sense=x["sensor_type"]
                flag=0
                for y in diction["sensors"]:
                    if(y["sensor_type"]==sense):
                        y["instance"].append(str(x["_id"]))
                        flag=1
                        break

                if flag == 0 :
                    diction["sensors"].append({"sensor_type" : sense ,"instance" : [str(x["_id"])]})
        loc_info.append(diction)
    for x in loc_info:
        for y in stsen:
            flag=0
            for z in x["sensors"]:
                if(z["sensor_type"]==y):
                    flag=1
                    break
            if flag==0:
                x["sensors"].append({"sensor_type": y ,"instance" : []})


    print(loc_info)
    

    
    return {"response":loc_info}



@app.route('/list_sensor_info_by_loc')
def list_sensor_info_by_loc():
    '''
    {
        "resp": [
            {
                "location": "bakul",
                "sensor_ins": [ "1234", "1246" ],
                "sensor_type": "heat"
            },
            {
                "location": "OBH",
                "sensor_ins": [ "3212", "2246" ],
                "sensor_type": "camera"
            }
        ]
    }
    '''



    all = ins_info.find()
    alldata   = []

    for i in all:
        alldata.append(i)

    #print(alldata[0]["location"])
    stloc = set()
    stsen = set()
    # for i in range(len(alldata)):
    #     stloc.add(alldata[i]["location"])
    #     stsen.add(alldata[i]["sensor_type"])
    for x in alldata:
        stloc.add(x["location"])
        stsen.add(x["sensor_type"])

    stloc = list(stloc)
    stsen = list(stsen)
    ans = {}
    loc_info=[]
    # print(alldata)
    # print(stloc)
    for loc in stloc:
        diction=dict()
        diction["location"]=loc
        diction["sensors"]=[]
        for x in alldata:
            if(x["location"]!=loc):
                continue
            else:
                sense=x["sensor_type"]
                flag=0
                for y in diction["sensors"]:
                    if(y["sensor_type"]==sense):
                        y["instance"].append(str(x["_id"]))
                        flag=1
                        break

                if flag == 0 :
                    diction["sensors"].append({"sensor_type" : sense ,"instance" : [str(x["_id"])]})
        loc_info.append(diction)
    for x in loc_info:
        for y in stsen:
            flag=0
            for z in x["sensors"]:
                if(z["sensor_type"]==y):
                    flag=1
                    break
            if flag==0:
                x["sensors"].append({"sensor_type": y ,"instance" : []})

    print(loc_info)
    final=[]
    for i in range(len(loc_info)):
        loc = loc_info[i]["location"]
        li = loc_info[i]["sensors"] 
        
        for j in li:
            kans = {}
            kans["location"]=loc
            kans["sensor_type"] = j["sensor_type"]
            kans["sensor_ins"] = j["instance"]
            
            final.append(kans)

    return {"resp":final}

@app.route('/newsensorinfo_ap')
def newsensorinfo_ap():


    '''
    {
        "response":"success",
        "sensor_list": [
            {
                "sensor_location": "obh",
                "sensor_type": "camera",
                "sensor_output_type": "array",
                "sensor_instances":2
            },
            {
                "sensor_location": "bakul",
                "sensor_type": "heat",
                "sensor_output_type": "int",
                "sensor_instances":4
            }
        ]
    }
    '''
    
    
    
    all = ins_info.find()
    alldata   = []

    types=type_info.find()
    
    type_to_output=dict()
    for x in types:
        if x["output_type"] not in type_to_output:
            type_to_output[x["sensor_type"]]=x["output_type"]


    for i in all:
        alldata.append(i)

    stloc = set()
    stsen = set()
    

    for x in alldata:
        stloc.add(x["location"])
        stsen.add(x["sensor_type"])

    stloc = list(stloc)
    stsen = list(stsen)
    ans = {}
    loc_info=[]

    for loc in stloc:
        diction=dict()
        diction["location"]=loc
        diction["sensors"]=[]
        for x in alldata:
            if(x["location"]!=loc):
                continue
            else:
                sense=x["sensor_type"]
                flag=0
                for y in diction["sensors"]:
                    if(y["sensor_type"]==sense):
                        y["instance"].append(str(x["_id"]))
                        flag=1
                        break
                        
                if flag == 0 :
                    diction["sensors"].append({"sensor_type" : sense ,"instance" : [str(x["_id"])]})
        loc_info.append(diction)
    for x in loc_info:
        for y in stsen:
            flag=0
            for z in x["sensors"]:
                if(z["sensor_type"]==y):
                    flag=1
                    break
            if flag==0:
                x["sensors"].append({"sensor_type": y ,"instance" : []})
    

    instances=[]
    for x in loc_info:
        for y in x["sensors"]:
            diction=dict()
            diction["sensor_location"]=x["location"]
            diction["sensor_type"]=y["sensor_type"]
            diction["sensor_output_type"]=type_to_output[y["sensor_type"]]
            diction["sensor_instances"]=len(y["instance"])
            instances.append(diction)
    return {"sensor_list" : instances, "response" : "success"}




if(__name__ == "__main__"):
    
    init_sen()    # Initialize Old Sensors
    
    app.run(port=constants["PORT"]["SENSOR_PORT"], debug = True)
    

