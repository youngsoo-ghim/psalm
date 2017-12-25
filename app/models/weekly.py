#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
from __future__ import print_function # Python 2/3 compatibility
import decimal
import datetime
import json

import boto3
from flask import Flask, request, jsonify, session
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from app import app
from app.models.user.user import DecimalEncoder

dynamodb = boto3.resource(app.config["DB_CONNECT"])

class Weekly():
    """
        주보 조회
    """
    @staticmethod
    def get_weekly_paper(session):
        table = dynamodb.Table('Weekly')
        church_id = session['USER_INFO']['CHURCH_ID']
        #weekly_date = session['weekly_date']
        items = {}
        try:
            response = table.query(
                KeyConditionExpression=Key('church_id').eq(church_id)
                ,Limit=1
                ,ScanIndexForward = False
                #FilterExpression = Attr('church_name').eq('광림교회')
                #,ExpressionAttributeNames={"#yr": "year"},  # Expression Attribute Names for Projection Expression only.
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            if response['Count'] > 0:
                print(type(items))
                items = response['Items'][0]
                print("doLogin succeeded:")
                print(type(response['Items'][0]))
                print(type(items))
                print(items)
            else:
                print("getWeeklyPaper 사용자 정보 없음")
        return items