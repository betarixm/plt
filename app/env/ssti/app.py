# -*- coding: utf-8 -*-

import flask
import sys
import os

app = flask.Flask(__name__)

try:
    FLAG = open('./flag.txt', 'r').read()
except:
    FLAG = "Failed to open flag.txt. please retry."
app.secret_key = FLAG


@app.route('/', methods=['GET'])
def index():
    query = flask.request.args.get('query','')
    return flask.render_template_string("""%s""" % query)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=False)