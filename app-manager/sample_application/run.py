from flask import Flask, render_template
import sys
import api
# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
# from flask_apscheduler import APScheduler

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
    
@app.route("/")
def hello():
    with app.app_context():
        print("enter hello")
        x = []
        try:
            x = api.get_sensor_data(0)

        except Exception as e:
            print("something went wrong ", e)    
        
        if x is None or len(x) == 0 :
            print("\n\n ******************** \n\nkuch nhi \n **************** \n\n")
            x = [0.0, 0.0, 8.0, 14.0, 16.0, 16.0, 1.0, 0.0, 0.0, 6.0, 16.0, 16.0, 8.0, 3.0, 0.0, 0.0, 0.0, 14.0, 14.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 15.0, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 15.0, 16.0, 6.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 8.0, 15.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 13.0, 15.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 16.0, 4.0, 0.0, 0.0, 0.0]
        
        print("enter preprocess")
        print(x)


        x = api.pre_process(x)
    
        # x = [0.0, 0.0, 8.0, 14.0, 16.0, 16.0, 1.0, 0.0, 0.0, 6.0, 16.0, 16.0, 8.0, 3.0, 0.0, 0.0, 0.0, 14.0, 14.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 15.0, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 15.0, 16.0, 6.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 8.0, 15.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 13.0, 15.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 16.0, 4.0, 0.0, 0.0, 0.0]
        print("enter use model")
        x = api.use_model(0, x)
        print("enter post process")
        x = api.post_process(x)
        response = {
            "result":x
        }
        print(response)
        return render_template("index.html", result=response)
    

if __name__ == "__main__":
    print(sys.argv[1])
    app.run(host='0.0.0.0', port=sys.argv[1], debug=True)
    scheduler = BlockingScheduler()
    scheduler.add_job(func=hello, trigger='interval', id='job', seconds=5)
    scheduler.start()
    # atexit.register(lambda: scheduler.shutdown())
    # print("hello world")
