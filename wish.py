import requests
import json
import time
import sys
import os
# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
headers={}
def get_num_id(num,start,cals,head,query):
    r=requests.post("https://www.wish.com/api/search?start="+str(start)+"&query="+query+"&transform=true",headers=head)
    result = json.loads(r.text)
    for data in result["data"]["results"]:
        if "feed_tile_text" in data:
                num=data["feed_tile_text"].replace(" bought this","")
                num = num.strip("+")
                cal={}
                cal["num"]=num
                cal["id"]=data["id"]
                cals.append(cal)
    return len(result["data"]["results"])
def get_express(id):
        url="https://www.wish.com/api/related-feed/get?offset=0&count=30&feed_mode=express&contest_id="+id+"&log_request=false&_buckets=&_experiments="
        r=requests.post(url,headers)
        result = json.loads(r.text)
        return result
def cal_diff(keywords,pre,now):
        diffs=[]
        pre_date=os.path.join(APP_STATIC+"/"+keywords, pre)
        #print(pre_date)
        now_date=os.path.join(APP_STATIC+"/"+keywords, now)
        pres=[]
        with open(pre_date,'r') as load_f:
                 pres = json.load(load_f)
        #print(pres)
        print(now_date)
        nows=[]
        with open(now_date,'r') as load_f:
                 nows = json.load(load_f)
        for now in nows:                
                for pre in pres:
                        if now["id"]==pre["id"]:
                                diff={}
                                diff["id"]= pre["id"]
                                incr = int(now["num"])-int(pre["num"])                                
                                diff["pre"]=pre["num"]
                                diff["now"]=now["num"]
                                diff["incr"]= incr
                                diffs.append(diff)
        return diffs
def add_keywords(keywords):
        with open(os.path.join(APP_STATIC+"/keywords.txt"),"a") as f:
                f.write("\n")
                f.write(keywords)
def get_keywords():
        results=[]
        with open(os.path.join(APP_STATIC+"/keywords.txt"),"r") as file:
                while 1:
                        line = file.readline()
                        if len(line.replace("\n",""))>0:
                                results.append(line.replace("\n",""))
                        if not line:
                                break
                        pass
        return results
def crawlwish(date,query):
        print("start")
        headers ={"Cookie":"bsid=50d9fabb01ec49faad2e96a63aadf7d6"}
        r=requests.get("https://www.wish.com",headers=headers)
        xsrf = r.cookies.get_dict()["_xsrf"]
        bsid = r.cookies.get_dict()["bsid"]
        headers={}
        headers["X-XSRFToken"]=xsrf
        headers["Cookie"]='bsid='+bsid+'; _xsrf='+xsrf+';'
        r=requests.post("https://www.wish.com/api/email-login?email=1530947234%40qq.com&password=cgdsxt007%26&_buckets=&_experiments=",headers=headers) 
        cookie =r.cookies.get_dict()
        headers["Cookie"]+="sweeper_session="+cookie["sweeper_session"]+";"
        #product_ids =[]
        cals=[]
        start =0
        while(start<500):
                print(start)
                start+=get_num_id(10,start,cals,headers,query)
        with open(os.path.join(APP_STATIC+"/"+query, date+".json"),"w") as f:
                json.dump(cals,f)
#crawlwish("20180612","phone+case")
        


