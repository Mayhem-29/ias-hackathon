from flask import Flask,render_template,request,redirect
import random
import json
import random
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from ensurepip import bootstrap
import time
import threading
import pymongo
from utils import topics 



import dns
# ***************************************** Kafka *********************************************************


from kafka.admin import KafkaAdminClient, NewTopic
from kafka.consumer import KafkaConsumer
from kafka import KafkaProducer



cluster = pymongo.MongoClient('mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority')
db = cluster["Hackathon"]
type_info = db["type_info"]
ins_info = db["ins_info"]



# IP_ADDR = "0.0.0.0:9092"
IP_ADDR = "13.71.94.55:9092"



def serialize(msg):
        return json.dumps(msg).encode('utf-8')

IP_ADDR = "13.71.94.55:9092"

producer = KafkaProducer(
    bootstrap_servers = [IP_ADDR],
    value_serializer = serialize
)


def data_producer(topic,data_type):
    topics.create_topic(topic)
    
    producer = KafkaProducer(
        bootstrap_servers = ["13.71.94.55:9092"],
        value_serializer = serialize
    )
    if(data_type=="int"):
        while True:
            msg = random.randint(10,10000)
            producer.send(topic,msg)
            # print("Producer : ", msg)
            time.sleep(random.randint(1,5))
    elif(data_type == "float"):
        while True:
            msg = int(random.random()*100)/100
            producer.send(topic,msg)
            # print("Producer : ", msg)
            time.sleep(random.randint(1,5))

IP_ADDR = "13.71.94.55:9092"







##################################################################################################################




# engine=create_engine("mysql+pymysql://root:mast1320@localhost/iasdb")
# db=scoped_session(sessionmaker(bind=engine))


# app=Flask(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = "sensor_manager"




def generateint():
    return random.randint(10,10000)

def generatefloat():
    return int(random.random()*100)/100



@app.route("/")
def home():
    #type_info.insert_one({"_id":0, "user_name":"Soumi"})
    return {"Marmik":"2009"}

@app.route('/installsensor')
def installsensor():
    return render_template('installsensor.html')


@app.route('/install_sensortype', methods=["POST"])
def install_sensortype():
    if request.method=="POST":
        sensor_type=request.form.get("sensor_type")
        # nout=request.form.get("nof")
        output_type=request.form.get("output_type")
        
        
        q1 = { "sensor_type": sensor_type }

        
        # mdl = type_info.query.get(sensor_type)
        mdl = type_info.find(q1)
        
        alldata=[]
        
        for i in mdl:
            alldata.append(mdl)
            
        
        print(mdl)
        if(len(alldata)==0):
            #model = type_info(sensor_type=sensor_type,output_type=output_type)
            type_info.insert_one({"sensor_type":sensor_type, "output_type":output_type})
   
    return redirect('/installsensor')


@app.route('/appdev_insert_type/<string:sensor_type>/<string:output_type>')
def appdev_insert_type(sensor_type,output_type):
    
    q1 = { "sensor_type": sensor_type }

    
    # mdl = type_info.query.get(sensor_type)
    mdl = type_info.find(q1)
    
    alldata=[]
    
    for i in mdl:
        alldata.append(mdl)
        
    
    print(mdl)
    if(len(alldata)==0):
        #model = type_info(sensor_type=sensor_type,output_type=output_type)
        type_info.insert_one({"sensor_type":sensor_type, "output_type":output_type})
    ans = {"response":"ok"}
    return ans
    
    
    
    



@app.route('/install_sensorins', methods=["POST"])
def install_sensorins():
    if request.method=="POST":
        sensor_type=request.form.get("sensor_type")
        location=request.form.get("location")
        q1={"sensor_type": sensor_type}
        mdl=type_info.find(q1)
        flag=0
        for x in mdl:
            if(x["sensor_type"]==sensor_type):
                flag=1
                break
        if(flag==1):
            ins_info.insert_one({"sensor_type": sensor_type , "location" : location})
        
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
        
        
        t = threading.Thread(target=data_producer, args=[ins_id,d_type])
        t.start()
             
    return redirect('/installsensor')            

@app.route('/getKafkaTopicForSensorData/<string:s_info>')
def getKafkaTopicForSensorData(s_info):
    
    sensor_type,location,noi = s_info.split(',')
    noi = int(noi)
    # f = open('data.json')
 
    # insid = db.execute("SELECT ins_id from ins_info WHERE sensor_name=:sensor_name and loc=:loc ",{"sensor_name":sensor_name, "loc":loc}).fetchall()
    
    missing = ins_info.query.filter_by(sensor_type=sensor_type, location= location  ).first()
    data={}
    # data["li"]=insid[0:noi]
    return data


@app.route('/getsensordata/<string:s_info>')
def getsensordata(s_info):
    
    sensor_type,location,noi = s_info.split(',')
    noi = int(noi)
    # f = open('data.json')
    #insid = ins_info.query.filter_by(sensor_type=sensor_type, location= location  ).all()
    q1={"sensor_type" : sensor_type , "location" : location}
    insid = ins_info.find(q1)
    # insid = db.execute("SELECT ins_id from ins_info WHERE sensor_type=:sensor_type and location=:location ",{"sensor_type":sensor_type, "location":location}).fetchall()
    print("aa gaya")
    ans={}
    # f = open('sensor_info.json')
    # sinfo = json.load(f)
    # f.close()
    q2={"sensor_type" : sensor_type}
    data_type=type_info.find(q2)
    
    data_type = type_info.query.filter_by(sensor_type=sensor_type ).first()
    # data_type = db.execute("SELECT output_type from type_info WHERE sensor_type=:sensor_type ",{"sensor_type":sensor_type}).fetchone()
    print("aa gaya")

    for i in range(noi):
        if(data_type.output_type=='int'):
            ans[i]={}
            ans[i]["ins_id"]=insid[i].ins_id
            ans[i]["data"]=random.randint(10,10000)
            # ans[insid[i][0]]=random.randint(10,10000)
        elif(data_type.output_type=='float'):
            ans[i]={}
            ans[i]["ins_id"]=insid[i].ins_id
            ans[i]["data"]=int(random.random()*100)/100
            # ans[insid[i][0]]=int(random.random()*100)/100
    print(ans)

    return ans




@app.route('/get_sensor_info')
def get_sensor_info():

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
        print(x["_id"])
        print(str(x["_id"]))

    stloc = list(stloc)
    stsen = list(stsen)
    ans = {}
    for loc in stloc:
        ans[loc]={}
        for s_type in stsen:
            ans[loc][s_type]=[]

    # for i in range(len(alldata)):
    #     ans[alldata[i]["location"]][alldata[i]["sensor_type"]].append(alldata[i]["ins_id"])

    print(ans["hyd"]["mic"])
    print(alldata)

    for x in alldata:
        print(x)
        ans[x["location"]][x["sensor_type"]].append(str(x["_id"]))
        print(type(str(x["_id"])))

    return ans


@app.route('/newsensorinfo')
def newsensorinfo():

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
    return {"resp":loc_info}



@app.route('/newsensorinfo_ap')
def newsensorinfo_ap():

    all = ins_info.find()
    alldata   = []

    types=type_info.find()
    
    type_to_output=dict()
    for x in types:
        if x["output_type"] not in type_to_output:
            type_to_output[x["sensor_type"]]=x["output_type"]
            

    print(type_to_output)

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
    

    instances=[]
    for x in loc_info:
        for y in x["sensors"]:
            diction=dict()
            diction["sensor_location"]=x["location"]
            diction["sensor_type"]=y["sensor_type"]
            diction["sensor_output_type"]=type_to_output[y["sensor_type"]]
            diction["sensor_instances"]=len(y["instance"])
            instances.append(diction)
    return {"sensor_list" : instances}


if(__name__ == "__main__"):
    #db.create_all()
    app.run(port="8011", debug = True)





