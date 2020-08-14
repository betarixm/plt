# -*- coding: utf-8 -*-

import flask
import os
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)


@app.route('/', methods=['GET'])
def index():
    flask.request.args.get('query','')
    return flask.render_template_string("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=False)