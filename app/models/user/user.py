#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
from __future__ import print_function # Python 2/3 compatibility
import json
import decimal
import datetime

import boto3
from flask import Flask, request, jsonify
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from app import app


# app = Flask('psalm')
#
# app.config.from_object('config')
dynamodb = boto3.resource(app.config["DB_CONNECT"])
userTable = "psalm_User"
# Helper class to convert a DynamoDB item to JSON.

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class User:
    def __init__(self, request):
        self.request = request
        self.table = dynamodb.Table(userTable)

        self.account_email = request.values['account_email']
        self.pwd = request.values['pwd']
        self.lastname = request.values['lastname']
        self.firstname = request.values['firstname']

        #사용시간 set
        now = datetime.datetime.now()
        self.reg_date = now.strftime('%Y-%m-%d %H:%M:%S')
        self.update_date = now.strftime('%Y-%m-%d %H:%M:%S')

    """
    사용자 정보 입력 메소드 작성
    """
    #@staticmethod
    #@classmethod
    def insert_user_info( self ):
        app.logger.info(self)
        try:
            response = self.table.put_item(
                Item={
                    'account_email': self.account_email
                    ,'pwd': self.pwd
                    ,'lastname': self.lastname
                    ,'firstname': self.firstname
                    ,'reg_date': self.reg_date
                    ,'update_date': self.update_date
                    ,'role': 'shepherd'
                    #,'church_id': church_id
                }
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            app.logger.info("insert_user_info succeeded:")
            print(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))


    """
    사용자 정보 update
    """
    @staticmethod
    def update_user_info(request, account_email, church_id):
        table = dynamodb.Table(userTable)

        ue = 'set '
        eav = {}
        setValueCount = 0

        # if('account_email' in request):
        #     account_email = request.values['account_email']
        #     ue = setQueryComma(setValueCount, ue)
        #     ue += "account_email = :ae"
        #     eav[':ac'] = account_email
        if('pwd' in request.values):
            pwd = request.values['pwd']
            (ue, setValueCount) = input_comma_query(setValueCount, ue)
            ue += "pwd = :pw "
            eav[':pw'] = pwd
        if('lastname' in request.values):
            lastname = request.values['lastname']
            (ue, setValueCount) = input_comma_query(setValueCount, ue)
            ue += "lastname = :ln "
            eav[':ln'] = lastname
        if('firstname' in request.values):
            firstname = request.values['firstname']
            (ue, setValueCount) = input_comma_query(setValueCount, ue)
            ue += "firstname = :fn"
            eav[':fn'] = firstname
        if('church_id' in request.values):
            #church_id = request.values['church_id']
            (ue, setValueCount) = input_comma_query(setValueCount, ue)
            ue += "church_id = :ci"
            eav[':ci'] = church_id

        # 위에서 처리한 값에 마지막 update 시간 추가
        (ue, setValueCount) = input_comma_query(setValueCount, ue)
        ue += "update_date = :ud"
        eav[':ud'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            response = table.update_item(
                Key={
                    'account_email': account_email
                },
                UpdateExpression=ue,
                ExpressionAttributeValues=eav,

                ReturnValues = "UPDATED_NEW"
            )
            # UpdateExpression = "set info.rating = :r, info.plot=:p, info.actors=:a",
            # ExpressionAttributeValues = {
            #                                 ':r': decimal.Decimal(5.5),
            #                                 ':p': "Everything happens all at once.",
            #                                 ':a': ["Larry", "Moe", "Curly"]
            #                             },

        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            app.logger.info("update_user_info succeeded:")
            app.logger.info(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))


    """
    사용자 확인 존제 확인
    """
    @staticmethod
    def get_user(request):
        table = dynamodb.Table(userTable)
        account_email = request.values['account_email']
        item = []
        try:
            response = table.get_item(
                Key={
                    'account_email': account_email
                }
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            if 'Item' in response:
                item = response['Item']
                app.logger.info("get_user succeeded:")
                app.logger.debug(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))
                app.logger.debug(jsonify(response))
            else:
                app.logger.info("get_user 사용자 정보 없음")

        return item

    """
    사용자 id로 정보 조회
    """
    @staticmethod
    def get_user_for_id(account_email):
        table = dynamodb.Table(userTable)
        #account_email = request.values['account_email']
        item = []
        try:
            response = table.get_item(
                Key={
                    'account_email': account_email
                }
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            if 'Item' in response:
                item = response['Item']
                app.logger.info("get_user_for_id succeeded:")
                app.logger.debug(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))
                app.logger.debug(jsonify(response))
            else:
                app.logger.info("get_user_for_id 사용자 정보 없음")

        return item


    """
    사용자 로그인
    """
    @staticmethod
    def do_login(request):
        table = dynamodb.Table(userTable)
        account_email = request.values['account_email']
        pwd = request.values['pwd']
        items = {}
        try:
            response = table.query(
                KeyConditionExpression=Key('account_email').eq(account_email)
                ,FilterExpression = Attr('pwd').eq(pwd)
                #,ExpressionAttributeNames={"#yr": "year"},  # Expression Attribute Names for Projection Expression only.
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            if response['Count'] > 0:
                print(type(items))
                items = response['Items'][0]
                app.logger.info("do_login succeeded:")
                app.logger.debug('account_email : %s' % account_email)
                app.logger.debug(type(response['Items'][0]))
                app.logger.debug(items)
            else:
                app.logger.info("do_login 사용자 정보 없음")
        return items


"""
dynamodb 쿼리시 해당 UpdateExpression 에 각각의 값을 동적으로 구성 할 때 콤마로 구분이 필요
해당 처리를 위한 콤마 생성기
"""
def input_comma_query(setValueCount, ue):
    if (setValueCount > 0):
        ue += ', '
    setValueCount += 1
    return ue, setValueCount