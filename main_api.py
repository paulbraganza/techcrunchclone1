#IMPORTS FOR FLASK AND HANDLING REQUESTS
from flask import Flask,jsonify,request
import re
import json
import tech_crunch_API
#INITIALIZING APP
app = Flask(__name__)
a=['apps','gadgets','startups']
#DEFUALT DASHBOARD SHOWS ALL APP NEWS 
@app.route('/')
def get():
    src = request.args.get('src')
    page=request.args.get('page')
    data=tech_crunch_API.scrape(src,page)
    response=jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/search')
def search():
    keywords = request.args.get('key')
    page=request.args.get('page')
    keywords=keywords.upper()
    keywords=keywords.split(" ")
    data=[]
    data1=[]
    for i in a:
        data.extend(tech_crunch_API.scrape(i,page))
    for d in data:
        title=d.get("post_title")
        desc=d.get("post_desc")
        title=title.upper()
        desc=desc.upper()
        title=title+" "+desc
        for k in keywords:
            if k in title:
                data1.append(d)
    #to remove dublicate data
    seen = set()
    new_l = []
    for d in data1:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    response=jsonify(new_l)
    response.headers.add('Access-Control-Allow-Origin', '*')   
    return response


if __name__ == '__main__':
    app.run(debug=True)

