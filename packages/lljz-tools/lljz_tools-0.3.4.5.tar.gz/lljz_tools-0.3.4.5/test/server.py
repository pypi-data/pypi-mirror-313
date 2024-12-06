# coding=utf-8

"""
@fileName       :   server.py
@data           :   2024/8/28
@author         :   jiangmenggui@hosonsoft.com
"""
from flask import Flask, request

from lljz_tools.c_random import random_string

app = Flask(__name__)

tokens = set()


@app.route('/')
def hello_world():
    token = request.headers.get('token')
    if token not in tokens:
        return 'error!'
    return 'welcome!'


@app.route('/a')
def a():
    return 'a'


@app.route('/b')
def b():
    return 'b'


@app.route('/login')
def login():
    token = random_string(10)
    tokens.add(token)
    return token


if __name__ == '__main__':
    app.run(port=5000, debug=True)
