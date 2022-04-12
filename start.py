import json
import shutil
import os
f = open('constants.json')
data = json.load(f)
dict = {"SENSOR": "Sensor\ Manager",
        "MODEL": "AI\ Manager",
        "LOAD": "LoadBalancer",
        "APP": "app-manager",
        "DEPLOYER": "Deployer",
        "NODE": "NodeManager",
        "SCHEDULER": "Scheduler",
        "AUTH": "Auth\ Manager"}
for service in data['LIST']:
    port = data["PORT"][service+"_PORT"]
    filename = data["FILES"][service+"_FILE"]
    destination = "/"+dict[service]
    cmd = "python3 docker_file_generator.py "+port+" "+destination+" "+filename
    os.system(cmd)
