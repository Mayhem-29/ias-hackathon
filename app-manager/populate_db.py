from pymongo import MongoClient

DB_SERVER = "mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority"
client = MongoClient(DB_SERVER)
HACKATHON_DB = client['Hackathon']

AppDB = HACKATHON_DB['AppInfo']

val = {
    "app_name": "ExApp",
    "app_author": "Example Author",
    "app_path": "/path/to/app",

    "models": [
        {
            "model_id": "model_id_1",
            "model_name": "model_name_1"
        },
        {
            "model_id": "model_id_2",
            "model_name": "model_name_2"
        }
    ],

    "sensors": [
    {
        "sensor_type":"A",
        "sensor_instances":"3"

    },
    {
        "sensor_type":"B",
        "sensor_instances":"2"
    }
    ]

}

AppDB.insert_one(val)