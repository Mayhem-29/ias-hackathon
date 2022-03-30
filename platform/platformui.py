import requests
import datetime

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
    applist = req_sess.get(endpoint["app_manager"]["base_url"] + endpoint["app_manager"]["uri"]["get_all_apps"]).json()
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
         
    resp = req_sess.post(endpoint["app_manager"]["base_url"] + endpoint["app_manager"]["uri"]["deploy_app"], json=x).json()

    return resp


def init():
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


import subprocess
# subprocess.call(['open', '-W', '-a', 'Terminal.app', 'python', '--args', '--version'])


