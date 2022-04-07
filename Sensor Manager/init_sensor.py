from kafka.admin import KafkaAdminClient, NewTopic
from kafka.consumer import KafkaConsumer
from kafka import KafkaProducer
import pymongo
import time 
import random
import json
import threading


cluster = pymongo.MongoClient('mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority')
db = cluster["Hackathon"]
type_info = db["sensor_type_info"]
ins_info = db["sensor_instance_info"]

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


def data_producer_init(topic,data_type):
    
    
    producer = KafkaProducer(
        bootstrap_servers = [IP_ADDR],
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

def init_sen():
    
    all = ins_info.find()

    for i in all:
        topic_n = str(i["_id"])
        sensor_type = i["sensor_type"]
        q1 = {"sensor_type":sensor_type}
        ab = type_info.find(q1)
        d_type = ""
        for x in ab:
            d_type = x["output_type"]
        
        t = threading.Thread(target=data_producer_init, args=[topic_n,d_type])
        t.start()
    