#!/usr/bin/env python
# FIlename: pyRestDb.py

'''
Created on 18 Dec 2013

@author: rmamba@gmail.com
'''

import asyncore
import json

from flask import Flask
from flask import request
app = Flask(__name__)
data = {}

@app.route('/')
def list_variable(variable=None, value=None):
    #data['args'] = request.args
    pjson = False
    return return_data(data, pjson)

@app.route('/<variable>')
def show_value(variable=None):
    data['args'] = request.args
    pjson = False
    try:
	val = data[variable]
        return return_data(val, pjson)
    except IndexError:
        return return_data({"response": "EMPTY"},pjson)

@app.route('/<variable>/<value>')
def handle_variable(variable=None, value=None):
    data['args'] = request.args
    pjson = False
    try:
	data[variable] = json.loads(value)
	return return_data({"response": "OK"}, pjson)
    except Exception,e:
	return return_data({"error": e}, pjson)

def return_data(data, pjson=False):
    return json.dumps(data)

if __name__ == '__main__':
    _host = '0.0.0.0'
    _port = 666
    app.debug = True
    app.run(host=_host, port=_port)
