import boto3

from app import app

dynamodb = boto3.resource(app.config["DB_CONNECT"])