#!/usr/bin/env python
# FIlename: pyRestDb.py

'''
Created on 18 Dec 2013

@author: rmamba@gmail.com
'''

import sys
import json
import time
import numbers
import string
import random

# RaspberryPi: sudo apt-get install python-flask
# OpenSuse: zypper install python-flask
# Mac OSX: sudo easy_install Flask
import flask
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__, static_folder='static')
data = {}
secret = {}
#Change Admin password for deployment!!!
#Run server with --admin=newPassword
_admin = 'password'

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', data=data)

@app.route('/static/<path:file>')
def file(file=None):
    if file == 'favicon.ico':
        file = 'rmamba.jpg'
    return send_from_directory(app.static_folder, file)

@app.route('/get')
@app.route('/get/<path:variable>')
@app.route('/get/<path:variable>/')
def show_value(variable=None):
    pjson = False
    _secret = None
    if 'pjson' in request.args:
        pjson = True
    if 'secret' in request.args:
        _secret = request.args['secret']
    if _secret == None:
        val = data
        if variable != None:
            path = variable.split('/')
            for p in path:
                if p in val:
                    val = val[p]
                else:
                    val = None
                    break
        if val != None:
            return return_json(val, pjson)
    else:
        if _secret in secret:
            val = secret[_secret]
            if variable != None:
                path = variable.split('/')
                for p in path:
                    if p in val:
                        val = val[p]
                    else:
                        val = None
                        break
            if val != None:
                return return_json(val, pjson)
    return return_json({"response": "EMPTY"}, pjson)

@app.route('/post/<variable>', methods=['POST'])
def set_value_post(variable=None):
    pjson = False
    if 'pjson' in request.args:
        pjson = True
    if request.method != 'POST':
        return return_json({"error": "GET is not supported for this command"}, pjson)
    _secret = None
    if 'secret' in request.args:
        _secret = request.args['secret']
    if _secret == None:
        data[variable] = json.loads(request.data)
    else:
        if not _secret in secret:
            secret[_secret] = {}
        secret[_secret][variable] = json.loads(request.data)
    return return_json({"response": "OK"})

@app.route('/set/<variable>/<value>')
@app.route('/set/<variable>/<value>/')
def set_string_value(variable=None, value=None):
    if not isinstance(value, numbers.Number):
        if value[0] != '"' and value[0] != '{':
            value = '"' + value
        if value[-1] != '"' and value[-1] != '}':
            value = value + '"'
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
        time.sleep(5)
        return return_json({"error": "Wrong password!"}, pjson)
    # return render_template('index.html', data=data)
    # return return_json({ "public": data, "secret": secret }, pjson)
    return render_template('index.html', data={"public": data, "secret": secret})

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

@app.route('/generate/secret')
def generate_secret(password=None):
    pjson = False
    if 'pjson' in request.args:
        pjson = True
    newSecret = id_generator()
    while newSecret in secret:
        newSecret = id_generator()
    secret[newSecret] = {}
    return return_json({"secret": newSecret}, pjson)

def return_json(data, pjson=False, sortkeys=True, code=200):
    if pjson:
        return flask.Response(response=json.dumps(data, sort_keys=sortkeys, indent=4, separators=(',', ': ')),
                              status=code, mimetype='application/json')
    else:
        return flask.Response(response=json.dumps(data, sort_keys=sortkeys), status=code, mimetype='application/json')

@app.errorhandler(404)
def page_not_found(e):
    return return_json({'error': 'Page not Found!!!'}, False, True, 404)

@app.errorhandler(500)
def internal_error(e):
    return return_json({'error': 'Internal server Error!!!'}, False, True, 500)

def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

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
    except Exception as e:
        print("Error: " + str(e))
