import sys
import os


topic_name = str(sys.argv[1])
d_type = str(sys.argv[2])

with open("Sensors/"+topic_name+"_sensor.py", 'w') as f:

    f.write("from kafka_fun import *")
    # f.write("\n\ncreate_topic('"+ str(topic_name)+"')\n")

    f.write("\n\ndata_producer('"+ str(topic_name)+"','"+str(d_type)+"')")
    

os.system("gnome-terminal --title=" +topic_name +" -x python3 " + "Sensors/"+topic_name+"_sensor.py")



