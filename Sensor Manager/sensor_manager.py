from flask import Flask,render_template,request,redirect
import random
import json
import random
import time
import threading
import pymongo
# from topics import * 
from flask_cors import CORS, cross_origin
import jwt

# app = Flask(name)




import dns
# ************** Kafka ********************


from kafka.admin import KafkaAdminClient, NewTopic
from kafka.consumer import KafkaConsumer
from kafka import KafkaProducer



cluster = pymongo.MongoClient('mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority')
db = cluster["Hackathon"]
type_info = db["sensor_type_info"]
ins_info = db["sensor_instance_info"]

# sensor_type_info = db["type_info"]
# sensor_instance_info = db["ins_info"]

# IP_ADDR = "0.0.0.0:9092"
IP_ADDR = "13.71.94.55:9092"



def serialize(msg):
        return json.dumps(msg).encode('utf-8')

IP_ADDR = "13.71.94.55:9092"

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

def data_producer(topic,data_type):
    create_topic(topic)
    
    producer = KafkaProducer(
        bootstrap_servers = ["13.71.94.55:9092"],
        value_serializer = serialize
    )
    if(data_type=="int"):
        while True:
            msg = random.randint(10,10000)
            producer.send(topic,msg)
            # print("Producer : ", msg)
            time.sleep(2.5)
    elif(data_type == "float"):
        while True:
            msg = int(random.random()*100)/100
            producer.send(topic,msg)
            # print("Producer : ", msg)
            time.sleep(2.5)
    elif(data_type=='array'):
        while True:
            f=open("data.json")
            data = json.load(f)
            i = random.randint(0,4)
            msg=data[str(i)]
            producer.send(topic,msg)
            # print("Producer : ", msg)
            time.sleep(2.5)


        


IP_ADDR = "13.71.94.55:9092"







##################################################################################################################




# engine=create_engine("mysql+pymysql://root:mast1320@localhost/iasdb")
# db=scoped_session(sessionmaker(bind=engine))


# app=Flask(_name_)

app = Flask(__name__)
cors = CORS(app)
# app.config['SECRET_KEY'] = "sensor_manager"
app.config['SECRET_KEY'] = "dub_nation"
def generateint():
    return random.randint(10,10000)

def generatefloat():
    return int(random.random()*100)/100


def read_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

constants = read_json("constants.json")


@app.route("/")
@cross_origin()
def home():
    try:
        print(request.args['jwt'])
        token = request.args['jwt']
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        return render_template("installsensor.html")
    except:
        return redirect(constants["BASE_URL"] + constants["PORT"]["APP_PORT"] + constants["ENDPOINTS"]["APP_MANAGER"]["home"])
    


@app.route('/install_sensortype', methods=["POST"])
def install_sensortype():
    if request.method=="POST":
        sensor_type=request.form.get("sensor_type")
        output_type=request.form.get("output_type")
        
        
        q1 = { "sensor_type": sensor_type }

        
        mdl = type_info.find(q1)
        
        alldata=[]
        
        for i in mdl:
            alldata.append(i)
            
        
        print(mdl)
        if(len(alldata)==0):
            type_info.insert_one({"sensor_type":sensor_type, "output_type":output_type})
        
   
    return redirect('/')


@app.route('/appdev_insert_type/<string:sensor_type>/<string:output_type>')
def appdev_insert_type(sensor_type,output_type):
    
    q1 = { "sensor_type": sensor_type }

    
    # mdl = type_info.query.get(sensor_type)
    mdl = type_info.find(q1) 
    
    alldata=[]
    
    for i in mdl:
        alldata.append(i)
    
    
    print(mdl)
    if(len(alldata)==0):
        #model = type_info(sensor_type=sensor_type,output_type=output_type)
        type_info.insert_one({"sensor_type":sensor_type, "output_type":output_type})
    ans = {"response":"ok"}
    return ans
    
    

@app.route('/list_of_sensortypes')
def list_of_sensortypes():
    mdl=type_info.find()
    ans=[]
    for x in mdl:
        ans.append(x["sensor_type"])
    
    return {"response":ans}
    



@app.route('/install_sensorins', methods=["POST"])
def install_sensorins():
     if request.method=="POST":
         
        sensor_type=request.form.get("sensor_type")
        location=request.form.get("location")
        sensor_ip = request.form.get("sensor_ip")
        sensor_port = request.form.get("sensor_port")
        #  print("hello")
        # resp=request.get_json()
        #    #resp = resp['sensor_data'][0]
        # print(resp)
        # sensor_type= resp["sensor_type"]
        # location=resp["location"]
        # sensor_ip=resp["sensor_ip"]
        # sensor_port=resp["sensor_port"]
        print(sensor_type)
        q1={"sensor_type": sensor_type}
        mdl=type_info.find(q1)
        print(mdl)
        flag=0
        for x in mdl:
            print(x["sensor_type"])
            if(x["sensor_type"]==sensor_type):
                flag=1
                break
        print("hi")
        if(flag==1):
            print("here")
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


            t = threading.Thread(target=data_producer, args=[ins_id,d_type])
            t.start()
             
        return redirect("/")
     
    # redirect('/installsensor')            



@app.route('/getsensordata/<string:s_info>')
def getsensordata(s_info):
    
    sensor_type,location,noi = s_info.split(',')
    noi = int(noi)
    q1={"sensor_type" : sensor_type , "location" : location}
    insid = ins_info.find(q1)
    print("aa gaya")
    ans={}
    q2={"sensor_type" : sensor_type}
    data_type=type_info.find(q2)
    
    data_type = type_info.query.filter_by(sensor_type=sensor_type ).first()
    print("aa gaya")

    for i in range(noi):
        if(data_type.output_type=='int'):
            ans[i]={}
            ans[i]["ins_id"]=insid[i].ins_id
            ans[i]["data"]=random.randint(10,10000)
        elif(data_type.output_type=='float'):
            ans[i]={}
            ans[i]["ins_id"]=insid[i].ins_id
            ans[i]["data"]=int(random.random()*100)/100
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
    

    
    return {"response":loc_info}



@app.route('/list_sensor_info_by_loc')
def list_sensor_info_by_loc():

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
    return {"sensor_list" : instances, "response" : "success"}




if(__name__ == "__main__"):
    #db.create_all()
    app.run(port="9100", debug = True)