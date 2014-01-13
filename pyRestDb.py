#!/usr/bin/env python
# FIlename: pyRestDb.py

'''
Created on 18 Dec 2013

@author: rmamba@gmail.com
'''

import sys
import asyncore
import json
import time

#RaspberryPi: sudo apt-get install python-flask
#OpenSuse: zypper install python-flask
import flask
from flask import Flask, request, render_template
app = Flask(__name__, static_folder='static')
data = { }
secret = { }
_admin = 'password'

@app.route('/')
@app.route('/index.html')
def index():
	return render_template('index.html', data=data)

@app.route('/static/<path:file>')
def file(file=None):
	return send_from_directory(app.static_folder, filename)

@app.route('/get')
@app.route('/get/<path:variable>')
def show_value(variable=None):
	pjson = False
	_secret = None
	if 'pjson' in request.args:
		pjson = True
	if 'secret' in request.args:
		_secret = request.args['secret']
	if _secret == None:
		val = data
		if variable!=None:
			path = variable.split('/')
			for p in path:
				if p in val:
					val = val[p]
				else:
					val = None
					break
		if val!=None:
			return return_json(val, pjson)
	else:
		if _secret in secret:
			val = secret[_secret]
			if variable!=None:
				path = variable.split('/')
				for p in path:
					if p in val:
						val = val[p]
					else:
						val = None
						break
			if val!=None:
				return return_json(val, pjson)
	return return_json({"response": "EMPTY"}, pjson)

@app.route('/post/<variable>', methods=['POST'])
def set_value_post(variable=None):
	if request.method != 'POST':
		return return_json({"error": "GET is not supported for this command"}, pjson)
	_secret = None
	if 'secret' in request.args:
		_secret = request.args['secret']
	if _secret == None:
		data[variable] = json.loads(request.data)
	else:
		if not _secret in secret:
			secret[_secret] = { }
		secret[_secret][variable] = json.loads(request.data)
	return return_json({"response": "OK"})

@app.route('/set/<variable>/<value>')
def set_value(variable=None, value=None):
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
			secret[_secret] = { }
		secret[_secret][variable] = json.loads(value)
		return return_json({"response": "OK"}, pjson)

@app.route('/admin/<password>')
def admin(password=None):
	pjson = False
	if 'pjson' in request.args:
		pjson = True
	if _admin != password:
		time.sleep(5)
		return return_json({"error": "Wrong password!"}, pjson)
		#return render_template('index.html', data=data)
	#return return_json({ "public": data, "secret": secret }, pjson)
	return render_template('index.html', data={ "public": data, "secret": secret })

@app.route('/admin/delete/<password>/<variable>')
def admin_delete(password=None, variable=None):
	pjson = False
	_secret = None
	if 'pjson' in request.args:
		pjson = True
	if 'secret' in request.args:
		_secret = request.args['secret']
	if _admin != password:
		time.sleep(5)
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
		time.sleep(5)
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

def return_json(data, pjson=False, sortkeys=True):
	if pjson:
		return flask.Response(response=json.dumps(data, sort_keys=sortkeys, indent=4, separators=(',', ': ')), status=200, mimetype='application/json')
	else:
		return flask.Response(response=json.dumps(data, sort_keys=sortkeys), status=200, mimetype='application/json')

@app.errorhandler(404)
def page_not_found(e):
    return flask.jsonify(error=404, text=e), 404
   
@app.errorhandler(500)
def internal_error(e):
    return flask.jsonify(error=500, text=e), 500

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
				_port = int(tmp[1])
			if arg.startswith('--admin='):
				tmp = arg.split('=')
				_admin = tmp[1]
	
		app.run(host=_host, port=_port)
	except Exception,e:
		print "Error: " + str(e)
