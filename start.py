import json,shutil,os
f=open('constant.json')
data=json.load(f)
dict={"SENSOR":"Sensor\ Manager",
    "MODEL": "AI\ Manager",
    "PLATFORM": "",
    "APP": "app-manager",
    "DEPLOYER": "Deployer",
    "NODE": "NodeManager_LoadBalancer",
    "SCHEDULER":"Scheduler"}
for service in data['LIST']:
    port=data["PORT"][service+"_PORT"]
    filename=data["FILES"][service+"_FILE"]
    destination="/"+dict[service]
    cmd="python3 docker_file_generator.py "+port+" "+destination+" "+filename
    os.system(cmd)


    



