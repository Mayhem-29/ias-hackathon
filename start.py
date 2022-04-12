import json,shutil,os
f=open('constants.json')
data=json.load(f)
dict={"SENSOR":"Sensor_Manager",
    "MODEL": "AI_Manager",
    "LOAD": "LoadBalancer",
    "APP": "app-manager",
    "DEPLOYER": "Deployer",
    "NODE": "NodeManager",
    "SCHEDULER":"Scheduler",
    "AUTH":"Auth_Manager",
    "NOTIFICATION": "Notification_Manager",
    "CONTROLLER": "Controller_Manager"}
for service in data['LIST']:
    port=data["PORT"][service+"_PORT"]
    filename=data["FILES"][service+"_FILE"]
    destination="./"+dict[service]
    print(destination)
    shutil.copy('constants.json',destination)
    shutil.copy('servers.json',destination)
    cmd="python3 docker_file_generator.py "+port+" "+destination+" "+filename
    os.system(cmd)


    



