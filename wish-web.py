from flask import Flask
from flask import render_template
import time
import wish
import json
import schedule
import sys
import _thread
from apscheduler.schedulers.background import BackgroundScheduler
app=Flask(__name__)
label_yesterday=time.strftime("%Y%m%d",time.localtime(time.time()-24*60*60))+"_baught.json"
label_today=str(time.strftime("%Y%m%d", time.localtime())) +"_baught.json"
@app.route('/wish') 
@app.route('/wish/<keywords>')
def hello_world(keywords=None):
    if keywords==None:
        keywords="phone+case"
    start =time.strftime("%Y%m%d",time.localtime(time.time()-24*60*60))
    end=str(time.strftime("%Y%m%d", time.localtime()))
    return render_template('index.html',keywords=keywords,start=start,end=end)
@app.route('/wish/diff/<keywords>/<start>/<end>')
def wish_diff(keywords=None,start=None,end=None):
    result=[]
    try:
        if len(start)<8:
            start =time.strftime("%Y%m%d",time.localtime(time.time()-24*60*60))
        if len(end)<8:
            end=str(time.strftime("%Y%m%d", time.localtime()))
        if keywords==None:
            keywords="phone+case"
        res = wish.cal_diff(keywords,start+".json",end+".json")
        repeatId=[]
        for n in res:            
            if int(n["pre"])<100 and n["pre"]!=n["now"] and n['id'] not in repeatId:                
                result.append(n)
                repeatId.append(n["id"])
    except:
        print("Unexpected error:", sys.exc_info()[0])
    return json.dumps(result)
def job():
    print("start job")
    label_today=str(time.strftime("%Y%m%d", time.localtime()))
    wish.crawlwish(label_today,"phone+case")
    wish.crawlwish(label_today,"rings")
def schejob():
    schedule.every(10).seconds.do(job)
    while True:
       schedule.run_pending()
       time.sleep(1)
if __name__ == '__main__':
    _thread.start_new_thread(schejob,())
    app.run(host='0.0.0.0',port="9561",debug=True)
