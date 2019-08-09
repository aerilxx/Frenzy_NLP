#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:15:38 2019

@author: bingqingxie
"""

from flask import Flask, request, jsonify, url_for, render_template, send_from_directory, Response
from werkzeug.utils import secure_filename
from main_function import run_nlp_analysis
from blog_crawler import crawl_text, crawl_img
import json
import sys

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt'])


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
            text = crawl_text(url)
            images = crawl_img(url)
            # print(text)
            return render_template('crawlresult.html', link=url, text=text, images=images)


        except:
            text = "Caught an exception" + str(sys.exc_info()[0]) + " , " + str(sys.exc_info()[1])
            images = []
            return render_template('crawlresult.html', link=url, text=text, images=images)


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
            data['nlp'] = result
            jsondata = []
            jsondata.append(data)
            return json.dumps(jsondata, default=set_default, indent=4)

    except:
        text = "Caught an exception" + str(sys.exc_info()[0]) + " , " + str(sys.exc_info()[1])
        return json.dumps(text)

    # postman load testing purpose, provide url links as parameter


@app.route('/jmetertesting', methods=['GET'])
def jmetertesting():
    try:
        if 'url' in request.args:
            link = request.args['url']
            text = crawl_text(link)
            img = crawl_img(request.args['url'])
            result = run_nlp_analysis(text)
            data = {}
            data['text'] = text
            data['img'] = img
            data['nlp'] = result
            jsondata = []
            jsondata.append(data)
            return json.dumps(jsondata, default=set_default, indent=4)
        else:
            return 'please provide url'

    except:
        text = "Caught an exception" + str(sys.exc_info()[0]) + " , " + str(sys.exc_info()[1])
        return json.dumps(text)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port = 8080, debug = True)
    # app.run(host="127.0.0.1", port=8080, debug=True)





