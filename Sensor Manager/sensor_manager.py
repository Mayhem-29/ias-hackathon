from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import json

username = "root"
password = "Root1234"
server = "localhost:3306"
database = "platformdb"

# engine=create_engine("mysql+pymysql://root:root123@localhost/ias_hackathon")
engine=create_engine(f"mysql+pymysql://{username}:{password}@{server}/{database}")
db=scoped_session(sessionmaker(bind=engine))

app=Flask(__name__)

SENSOR_PORT = 9100
MODEL_PORT = 9200
PLATFORM_PORT = 9300

@app.route("/")
def home():
    return {"Marmik":"2009"}


@app.route('/getsensordata/<string:s_info>')
def getsensordata(s_info):
    
    tid,loc = s_info.split(',')
    tid = int(tid)
    loc = int(loc)
    f = open('data.json')
 
    insid = db.execute("SELECT insid from sinsdb WHERE tyid=:tid1 and loc=:loc1 ",{"tid1":tid, "loc1":loc}).fetchone()
    datadb = json.load(f)
    res = {"data":datadb[str(insid[0])]}
    return res


@app.route('/sensorinfo')
def sensorinfo():
    
    tid = db.execute("SELECT tyid from stypedb").fetchall()
    res={}
    res2={}
    sen_name = db.execute("SELECT sensor_name from stypedb").fetchall()
    ct=0
    for i in tid:
        res2[i[0]]=sen_name[ct][0]
        ct += 1
    print(tid)
    for i in tid:
        tp={}
        stid = db.execute("SELECT insid from sinsdb where tyid=:tid1",{"tid1":i[0]}).fetchall()
        for j in stid:
            loc1 = db.execute("SELECT loc from sinsdb where insid=:t",{"t":j[0]}).fetchone()
            tp[j[0]]=loc1[0]
        tp[i[0]]=res2[i[0]]
        res[i[0]]=tp
  
    return res

if __name__=="__main__":
    app.run(port=SENSOR_PORT, debug=True)