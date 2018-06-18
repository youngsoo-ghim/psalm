#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
import boto3
from flask import Flask, render_template, redirect, Blueprint

from app.models.user.user import reg_customer_info

app = Flask('psalm')
print __name__

bp = Blueprint('flaskr', __name__)


if __name__ == '__main__':
    print __name__
    print 'This program is being run by itself'
else:
    print 'I am being imported from another module'
    print __name__


##
#BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
#app.config.from_object(__name__)

## direct access to config file
#app.config.from_pyfile('../config.py')

## object access to config
app.config.from_object('config')

## not working why not access to file (동작 안함 확인 필요)
#app.config.from_envvar('../config.py', silent=True)

app.logger.debug(app.config['SQLALCHEMY_DATABASE_URI'])
dynamodb = boto3.resource(app.config['DB_CONNECT'])

@app.route('/a')
def hello():
    app.logger.debug('debugging log.....')
    #return redirect(url_for('login'))
    return redirect('/login')

@app.route('/logina')
def login():
    name = "test"
    #request.__setitem__(request, "name", name)
    #return render_template('customer/signin.html', name=name)
    return render_template('user/signin.html', name=name)

@app.route('/customer/fomrRegId')
def fomrRegId():
    return render_template('user/regId.html')

@app.route('/customer/regId')
def regId(request=None):
    reg_customer_info(request)
    return render_template('user/regId.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
