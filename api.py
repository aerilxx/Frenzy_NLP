#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:15:38 2019

@author: bingqingxie
"""

from flask import Flask, request, jsonify, render_template, Response, flash,redirect,url_for
from main_function import run_nlp_analysis
from blog_crawler import crawl_text, crawl_img, crawl_title
import json
import sys
import time
import sqlalchemy
import os


app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt'])
app.secret_key = "secret"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# remove emoji in text for NLP analysis
def deEmojify(inputString):
    # incase of brands_name contains special ascic value
    text = ''.join([i if ord(i) < 256 else ' ' for i in inputString])
    return text


# -----------front end------------- #
@app.route('/')
def main():
    return render_template('index.html')


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


# front end tester for upload a txt file, get NLP result
@app.route('/uploader', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return "plz submit a file"

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return "file cannot be empty"
    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        text = file.read().decode(encoding='utf-8', errors='strict')
        try:
            result = run_nlp_analysis(text)
            return jsonify(result)

        except:
            msg = "Caught an exception" + str(sys.exc_info()[0]) + " , " + str(sys.exc_info()[1])
            return msg


    else:
        return "please submit a valid file"


@app.route('/crawl')
def crawler():
    return render_template('crawler.html')


# front end for crawler
@app.route('/crawler', methods=['POST'])
def blogger_crawler():
    url = request.values['link']

    if url is None or url is '':
        # print('no url')
        return "wrong url"
    else:
        # print(url)
        try:
            start = time.time()
            text = crawl_text(url)
            images = crawl_img(url)
            end = time.time()
            # print(text)
            return render_template('crawlresult.html', link=url, text=text, images=images, time = end - start)

        except:
            text = "Caught an exception" + str(sys.exc_info()[0]) + " , " + str(sys.exc_info()[1])
            images = []
            return render_template('crawlresult.html', link=url, text=text, images=images)

db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = 'brands'
cloud_sql_connection_name = "frenzynlp:us-central1:brands"
#db_name = os.environ.get("DB_NAME")


# The SQLAlchemy engine will help manage interactions, including automatically
# managing a pool of connections to your database
db = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username='aeril',
        password='aeril',
        database=db_name,
        query={
            'unix_socket': '/cloudsql/{}'.format(cloud_sql_connection_name)
        }
    ),
	pool_size=5,
    max_overflow=2,
    pool_timeout=300,  
    pool_recycle=1000,  # 20 minutes
)

# display all brands in front end
@app.route('/brands', methods=['GET'])
def display_brands():
    brands = []
    with db.connect() as conn:
        # Execute the query and fetch all results
        all_brands = conn.execute(
            "SELECT BrandName FROM Brands "
            "ORDER BY BrandName ASC"
        ).fetchall()
        # Convert the results into a list of dicts representing brands
        for row in all_brands:
            brands.append(row[0])

    return render_template('brands.html',brands = brands)

# add brands in db
@app.route('/addBrands',methods = ['POST'])
def add_brand():
    brand = request.values['addbrand']
    if brand is None or brand is '':
        return "please provide a valid brand name."
    
    else:
        stmt = sqlalchemy.text(
                "INSERT IGNORE INTO Brands (BrandName)"
                "VALUES(:brand)"
                )
        try:
            with db.connect() as conn:
                conn.execute(stmt, brand = brand)
                return Response(status=200,response="Add the brand: {} successfully!".format(brand))
        
        except Exception as e:
            return Response(status=500,response="You can't add this brands, becasue {}!".format(e)) 


# delete brands in db
@app.route('/delBrands',methods = ['POST'])
def del_brand():
    brand = request.values['delbrand']
    if brand is None or brand is '':
        return "please provide a valid brand name."
    
    else:
        print(type(brand))
        stmt = sqlalchemy.text(
                "DELETE FROM Brands WHERE BrandName = :brand "
             )
        
        try:
            with db.connect() as conn:
                conn.execute(stmt,brand = brand)
                return Response(status=200,response="Delete the brand: {} successfully!".format(brand))
        
        except Exception as e:
            return Response(status=500,response="You can't delete this brands, becasue {}!".format(e))    
         

# -------------- terminal endpoint and test on postman -------------------- #

# fix error :TypeError: Object of type 'set' is not JSON serializable
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


# get text and images results
@app.route('/getcrawler', methods=['POST'])
def img_crawler():
    try:
        url = request.get_data().decode('utf8')
        data = {}
        images = crawl_img(url)
        data['img'] = images
        text = crawl_text(url)
        data['text'] = text
        jsondata = []
        jsondata.append(data)
        return json.dumps(jsondata, default=set_default, indent=4)
    except:
        text = "Caught an exception" + str(sys.exc_info()[0]) + " , " + str(sys.exc_info()[1])
        return json.dumps(text)


# receive blogger text in body, return nlp in json format
@app.route('/getnlp', methods=['POST'])
def run_nlp():
    try:
        data = request.get_data().decode('utf8')
        if data is None:
            return "no text submitted"
        else:
            result = run_nlp_analysis(deEmojify(data))
            return jsonify(result)
    except:
        text = "Caught an exception" + str(sys.exc_info()[0]) + " , " + str(sys.exc_info()[1])
        return json.dumps(text)


# input url in terminal, get NLP result
@app.route('/getnlpresult', methods=['POST'])
def get_nlp_result():
    try:
        url = request.get_data().decode('utf8')

        if url is None:
            return "wrong url"
        else:
            text = crawl_text(url)
            result = run_nlp_analysis(text)
            return jsonify(result)
    except:
        text = "Caught an exception" + str(sys.exc_info()[0]) + " , " + str(sys.exc_info()[1])
        return json.dumps(text)


# input url in terminal, get all result including images, text, NLP
@app.route('/getallresult', methods=['POST'])
def get_all_result():
    try:
        url = request.get_data().decode('utf8')
        if url is None:
            return "please provide a url"
        else:
            text = crawl_text(url)
            img = crawl_img(url)
            result = run_nlp_analysis(text)
            data = {}
            data['text'] = text
            data['img'] = img
            data['nlp'] = json.loads(result)
            jsondata = []
            jsondata.append(data)
            return json.dumps(jsondata, default=set_default, indent=4)

    except:
        text = "Caught an exception" + str(sys.exc_info()[0]) + " , " + str(sys.exc_info()[1])
        return json.dumps(text)

   

# final end point for whole system, provide url links as parameter, can be used on loadtesting
@app.route('/nlp', methods=['POST', 'GET'])
def jmetertesting():
    try:
        url = request.values['url']
     
        if 'preview-token' in url:
            url = url.rstrip('/')

        if url:
            text = crawl_text(url)
            img = crawl_img(url)
            title = crawl_title(url)
            result = run_nlp_analysis(text)
            data = {}
            data['Title'] = title
            data['Description'] = text
            data['Images'] = img
            data['NLP_Result'] = json.loads(result)
            jsondata = []
            jsondata.append(data)
            return json.dumps(jsondata, default=set_default, indent=4)
        else:
            return "request.values didn't work."
      
    except:
        text = "Caught an exception" + str(sys.exc_info()[0]) + " , " + str(sys.exc_info()[1])
        return json.dumps(text)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port = 8080, debug = True)
    # app.run(host="127.0.0.1", port=8080, debug=True)





