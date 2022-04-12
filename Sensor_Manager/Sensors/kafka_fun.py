import sys
import json
import random
import time


CONST=""
with open("constants.json","r") as f:
    CONST = json.load(f)

# ***************************************** Kafka *********************************************************

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.consumer import KafkaConsumer
from kafka import KafkaProducer

IP_ADDR = CONST["KAFKA_HOST_ADDR"]

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
        print("Already Created or Something went wrong")
        return False

def data_producer(topic,data_type):
    
    # if(fg==1):
    create_topic(topic)
    print("\n\n")
    print("________________________________________________________\n")
    print("                     "+str(topic)+"                     \n")
    print("________________________________________________________\n")
    print("\n")
    producer = KafkaProducer(
        bootstrap_servers = [IP_ADDR],
        value_serializer = serialize
    )
    if(data_type=="int"):
        while True:
            msg = random.randint(10,10000)
            print(msg)
            producer.send(topic,msg)
            # print("Producer : ", msg)
            time.sleep(2.5)
    elif(data_type == "float"):
        while True:
            msg = int(random.random()*100)/100
            print(msg)
            producer.send(topic,msg)
            # print("Producer : ", msg)
            time.sleep(2.5)
    elif(data_type=='array'):
        while True:
            f=open("data.json")
            data = json.load(f)
            i = random.randint(0,4)
            msg=data[str(i)]
            print(msg)
            producer.send(topic,msg)
            # print("Producer : ", msg)
            time.sleep(2.5)


admin_client = KafkaAdminClient(
    bootstrap_servers = [IP_ADDR]
)     


# ********************************************** INIT Kafka  **********************************************

