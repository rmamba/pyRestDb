#!/usr/bin/env python
# FIlename: pyRestDb.py

'''
Created on 18 Dec 2013

@author: rmamba@gmail.com
'''

import sys
import asyncore
import json

from flask import Flask
from flask import request
app = Flask(__name__)
data = { }
secret = { }
_admin = 'password'

@app.route('/')
def list_variable():
	#data['args'] = request.args
	pjson = False
	if 'pjson' in request.args:
		pjson = True
	return return_json(data, pjson)

@app.route('/<variable>')
def show_value(variable=None):
	#data['args'] = request.args
	pjson = False
	_secret = None
	if 'pjson' in request.args:
		pjson = True
	if 'secret' in request.args:
		_secret = request.args['secret']
	if _secret == None:
		if variable in data:
			return return_json(data[variable], pjson)
	else:
		if _secret in secret:
			if variable in secret[_secret]:
				return return_json(secret[_secret][variable], pjson)
	return return_json({"response": "EMPTY"}, pjson)

@app.route('/<variable>/<value>')
def set_value(variable=None, value=None):
	#data['args'] = request.args
	pjson = False
	_secret = None
	if 'pjson' in request.args:
		pjson = True
	if 'secret' in request.args:
		_secret = request.args['secret']
	if _secret == None:
		data[variable] = json.loads(value)
		return return_json({"response": "OK"}, pjson)
	else:
		if not _secret in secret:
			secret[_secret] = {}
		secret[_secret][variable] = json.loads(value)
		return return_json({"response": "OK"}, pjson)

@app.route('/admin/<password>')
def admin(password=None):
	pjson = False
	if 'pjson' in request.args:
		pjson = True
	if _admin != password:
		#time.sleep(.1)
		return return_json({"error": "Wrong password!"}, pjson)
	return return_json({ "public": data, "secret": secret }, pjson)

@app.route('/admin/delete/<password>/<variabla>')
def admin_delete(password=None, variable=None):
	pjson = False
	_secret = None
	if 'pjson' in request.args:
		pjson = True
	if 'secret' in request.args:
		_secret = request.args['secret']
	if _admin != password:
		time.sleep(1)
		return return_json({"error": "Wrong password!"}, pjson)
	
	if _secret == None:
		if variable in data:
			del data[variable]
			return return_json({"response": "OK"}, pjson)
	else:
		if _secret in secret:
			if variable in secret[_secret]:
				del secret[_secret][variable]
				return return_json({"response": "OK"}, pjson)
	return return_json({"response": "EMPTY"}, pjson)

@app.route('/admin/purge/<password>')
def admin_purge(password=None):
	pjson = False
	_secret = None
	if 'pjson' in request.args:
		pjson = True
	if 'secret' in request.args:
		_secret = request.args['secret']
	if _admin != password:
		time.sleep(1)
		return return_json({"error": "Wrong password!"}, pjson)
	
	if _secret == None:
		data.clear()
		secret.clear()
		return return_json({"response": "OK"}, pjson)
	else:
		if _secret in secret:
			del secret[_secret]
			return return_json({"response": "OK"}, pjson)
	return return_json({"response": "EMPTY"}, pjson)

def return_json(data, pjson=False):
	if pjson:
		return json.dumps(data, sort_keys = True, indent = 2, separators=(',', ': '))
	else:
		return json.dumps(data)

if __name__ == '__main__':
	_host = '0.0.0.0'
	_port = 666
	try:
		for arg in sys.argv:
			if arg == "--debug":
				app.debug = True
			if arg.startswith('--host='):
				tmp = arg.split('=')
				_host = tmp[1]
			if arg.startswith('--port='):
				tmp = arg.split('=')
				_port = tmp[1]
			if arg.startswith('--admin='):
				tmp = arg.split('=')
				_admin = tmp[1]
	
		app.run(host=_host, port=_port)
	except Exception,e:
		print "Error: " + str(e)
