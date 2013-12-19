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
data = { }

@app.route('/')
def list_variable():
	#data['args'] = request.args
	pjson = False
	if 'pjson' in request.args:
		pjson = True
	return return_data(data, pjson)

@app.route('/<variable>')
def show_value(variable=None):
	data['args'] = request.args
	pjson = False
	if 'pjson' in request.args:
		pjson = True
	if variable in data:
		return return_data(data[variable], pjson)
	else:
		return return_data({"response": "EMPTY"}, pjson)

@app.route('/<variable>/<value>')
def set_value(variable=None, value=None):
	data['args'] = request.args
	pjson = False
	if 'pjson' in request.args:
		pjson = True
	try:
		data[variable] = json.loads(value)
		return return_data({"response": "OK"}, pjson)
	except Exception,e:
		return return_data({"error": str(e)}, pjson)

def return_data(data, pjson=False):
	if pjson:
		return json.dumps(data, sort_keys = False, indent = 2, separators=(',', ': '))
	else:
		return json.dumps(data)

if __name__ == '__main__':
	_host = '0.0.0.0'
	_port = 666
	#app.debug = True
	app.run(host=_host, port=_port)
