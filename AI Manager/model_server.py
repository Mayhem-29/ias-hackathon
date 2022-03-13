from flask import Flask
from flask import session
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = "dub_nation"

username = "root"
password = "Root1234"
server = "localhost:3306"
database = "platformdb"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{server}/{database}"
app.config['SESSION_TYPE'] = "sqlalchemy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
sess = Session(app)

class Model_db(db.Model):

    model_name = db.Column(db.String(40), primary_key = True)   
    input_format = db.Column(db.String(10), nullable = False)
    output_format = db.Column(db.String(40), nullable = False)
    pkl_url = db.Column(db.String(200), nullable = False)

    def __init__(self, model_name,input_format,output_format,pkl_url):
        self.model_name = model_name
        self.input_format = input_format
        self.output_format = output_format
        self.pkl_url=pkl_url

def comm(model):
    db.session.add(model)
    db.session.commit()

@app.route("/model", methods=['POST'])
def model_store():
    req = request.get_json()
    mdl = Model_db.query.get(req['model_name'])

    if(mdl == None):
        model = Model_db(req['model_name'], req['input_format'], req['output_format'],req['pkl_url'])
        comm(model)
        return "model stored"       
    
    else:
        return "model already exists"

if(__name__ == "__main__"):
    db.create_all()
    app.run(port="8000", debug = True)