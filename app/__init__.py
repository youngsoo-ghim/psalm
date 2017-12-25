from flask import Flask
from flask_httpauth import HTTPBasicAuth
import boto3
#from app.routes.index import *

app = Flask('psalm')
auth = HTTPBasicAuth()
#app = Flask(__name__)

app.config.from_object('config')
dynamodb = boto3.resource(app.config["DB_CONNECT"])
