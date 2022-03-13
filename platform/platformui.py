import requests


req_sess = requests.Session()


endpoint = {
    "app_manager": {
        "base_url": "",
        "uri": {
            "get_all_models_sensos": "/get_models_sensors",
            "get_all_apps": "/get_all_applications",
            "get_sensor_by_app_id": "/get_sensor_by_app_id",
            "deploy_app": "/deploy"
        }
    },
    "sensor_manager": {
        "base_url": "",
        "uri": {
            "": ""
        }
    },
    "model_manager": {
        "base_url": "",
        "uri": {
            "": ""
        }
    },
    "platform_manager": {
        "base_url": "",
        "uri": {
            "": ""
        }
    },
    "node_manager": {
        "base_url": "",
        "uri": {
            "": ""
        }
    }

}


def app_dev():
    pass

def data_sci():
    pass

def user_fn():
    getAppList()
    pass

def getAppList():
    applist = requests.get(base+"applist").json()
    applist = applist['list']
    if len(applist) == 0:
        return "No apps found"

    print("Select one app from the following list")
    for i in range(len(applist)):
        print(applist[i][0], applist[i][1])

    appchoice = input("Enter app id you want to use:")
    # requests.post(base+applist,appchoice)
    x = {"app_id": appchoice, "location": "loc1", "start_time": "2:00pm",
         "end_time": "", "current_time": datetime.datetime.now()}
         
    resp = requests.post(base+"/sensorInstance", json=x)

    return resp



print("pick the role !!")
print("1. App Developer")
print("2. Data Scientist")
print("3. User")

val = int(input("Enter the corresponding value: "))

if(val == 1):
    print("Following are the App Developers options, pick the one you want !!")
    print("1. Deploy the app!")
    val = int(input("Enter the corresponding value: "))
    if(val == 1):
        path = input("Enter the path: ")
        #function call of app deployment
        app_dev()
elif(val == 2):
    print("Following are the Data Scientist options, pick the one you want !!")
    print("1. Deploy the model!")
    val = int(input("Enter the corresponding value: "))
    if(val == 1):
        path = input("Enter the path: ")
        #function call of model deployment
        data_sci()
elif(val == 3):
    print("Following are the User options, pick the one you want !!")
    print("1. Run the app!")
    val = int(input("Enter the corresponding value: "))
    if(val == 1):
        path = input("Enter the path: ")
        #function call to run the app
        user_fn()
else:
    print("error encountered !!")