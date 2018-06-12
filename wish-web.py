from flask import Flask
from flask import render_template
import time
import wish
import json
from apscheduler.schedulers.background import BackgroundScheduler
app=Flask(__name__)
@app.route('/wish') 
@app.route('/wish/<name>')
def hello_world(name=None):
    return render_template('index.html',name=name)
@app.route('/wish/diff')
def wish_diff():
    label_yesterday=time.strftime("%Y%m%d",time.localtime(time.time()-24*60*60))+"_baught.json"
    label_today=str(time.strftime("%Y%m%d", time.localtime())) +"_baught.json"
    #diffs=[]
    #crawlwish()
    result=[]
    try:
        res = wish.cal_diff(label_yesterday,label_today)
        for n in res:
            #print(int(n["now"]))
            if int(n["pre"])<100:
                result.append(n)
    except:
        print("eror")
    print(len(result))
    return json.dumps(result)
if __name__ == '__main__': 
    scheduler = BackgroundScheduler()
    scheduler.add_job(wish.crawlwish, 'cron', hour=17,minute=25,second=3)
    scheduler.start()
    app.run(host='0.0.0.0',port="9561",debug=True)
