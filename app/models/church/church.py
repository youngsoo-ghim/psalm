#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
from __future__ import print_function # Python 2/3 compatibility
import json
import datetime
import decimal

import boto3
from flask import Flask, request, jsonify
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from app import app
from app.models.user.user import DecimalEncoder

dynamodb = boto3.resource(app.config["DB_CONNECT"])

class Church:
    def __init__( self, request ):
        self.request = request
        self.table = dynamodb.Table('Church')

        if request.values['church_name']:
            self.church_name = request.values['church_name']
        if request.values['zip_code']:
            self.zip_code = request.values['zip_code']
        if request.values['address']:
            self.address = request.values['address']
        if request.values['address_eng']:
            self.address_eng = request.values['address_eng']
        if request.values['address_detail']:
            self.address_detail = request.values['address_detail']


    """
    교회정보 입력
    """
    def insert_chruch( self, church_id ):

        now = datetime.datetime.now()

        reg_date = now.strftime('%Y-%m-%d %H:%M:%S')
        update_date = now.strftime('%Y-%m-%d %H:%M:%S')

        try:
            response = self.table.put_item(
                Item={
                    'church_id': church_id
                    ,'church_name': self.church_name
                    ,'zip_code': self.zip_code
                    ,'address': self.address
                    ,'address_eng': self.address_eng
                    ,'address_detail': self.address_detail
                    ,'reg_date': reg_date
                    ,'update_date': update_date
                }
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            print("regChruchInfo succeeded:")
            print(json.dumps(response, indent=4, cls=DecimalEncoder))

    """
    교회 조회
    """
    @staticmethod
    def get_church_info( request ):

        table = dynamodb.Table('Church')
        items = {}
        try:
            response = table.scan(
                FilterExpression = Attr('church_name')\
                    .contains(request.values['church_name'])
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            if response['Count'] > 0:
                items = response['Items']
                print(items)
                app.logger.info("getChurchInfo succeeded:")
                app.logger.info(json.dumps(response, indent=4, cls=DecimalEncoder))
            else:
                app.logger.info("getChurchInfo 교회 정보 없음")
        return items

"""
교회 id 생성 우편번호+_+yyyymmddhhmmss 22자 등
"""
def create_church_id(zipcode):
    now = datetime.datetime.now()
    return str(request.values['zip_code']) + "_" + str(now.strftime('%Y%m%d%H%M%S'))