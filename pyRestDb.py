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

@app.route('/<variable>/<value>')
def handle_variable(variable=None, value=None):
    print request.args
    pjson = False
    if variable == None:
        return return_data(data, pjson)
    else:
        if value == None:
            if data[variable] != None:
                return_data(data[variable], pjson)
            else:
                return_data({'DOES_NOT_EXIST'},pjson)
        else:
            data[variable] = json.loads(value)
            return_data({'OK'}, pjson)

def return_data(data, pjson=False):
    return json.dumps(data)

if __name__ == '__main__':
    _host = '127.0.0.1'
    _port = 666
    app.run(host=_host, port=_port)
