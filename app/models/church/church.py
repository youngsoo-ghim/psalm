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
churchTable = 'psalm_Church'

class Church:
    def __init__( self, request ):
        self.request = request
        self.table = dynamodb.Table(churchTable)

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
    def insert_chruch( self, church_id , session):

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
                    ,'official_yn': 'N'
                    ,'change_user_id': session['USER_INFO']['ACCOUNT_EMAIL'] # 없으면 에러
                }
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            app.logger.info("regChruchInfo succeeded:")
            app.logger.debug(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))

    """
    교회정보 업데이트
    """
    @staticmethod
    def update_church_info( request, session ):
        table = dynamodb.Table(churchTable)
        items = None

        now = datetime.datetime.now()
        update_date = now.strftime('%Y-%m-%d %H:%M:%S')

        inputKey = {'church_id': request.values['church_id']}
        ue = 'set church_name = :cn, zip_code = :zc, address = :ad' \
             ', address_eng = :ade, address_detail= :add, update_date = :ud '\
             ', change_user_id = :cui'
        eav = { ':cn':request.values['church_name']
                ,':zc':request.values['zip_code']
                ,':ad':request.values['address']
                ,':ade':request.values['address_eng']
                ,':add':request.values['address_detail']
                ,':ud':update_date
                ,':cui':session['USER_INFO']['ACCOUNT_EMAIL']}
        try:
            response = table.update_item(
                Key = inputKey
                , UpdateExpression = ue
                , ExpressionAttributeValues = eav
                , ReturnValues = "UPDATED_NEW"
            )

        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            app.logger.info("update_church_info succeeded:")
            app.logger.info(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))

    """
    교회 조회
    """
    @staticmethod
    def get_church_info( request ):

        table = dynamodb.Table(churchTable)
        items = {}
        try:
            response = table.scan(
                #IndexName = "church_name-index"
                # ,KeyConditionExpression = 'contains(church_name, :c)'
                # ExpressionAttributeValues = {
                #     ":c" : request.values['church_name']
                # }
                #,KeyConditionExpression = Key('church_name')\
                #     .begins_with(request.values['church_name'])
                #,QueryFilter = 'contains(church_name, :c)'

                #, ScanIndexForward = False
                #,KeyConditionExpression = Key('church_name').name(request.values['church_name'])
                #,KeyConditionExpression = 'contains(church_name, :name)'
                #,KeyConditionExpression = 'church_name = :name'
                #,ExpressionAttributeValues ={
                #    ":name" : request.values['church_name']
                #}
                FilterExpression = Attr('church_name').contains(request.values['church_name'])

            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            if response['Count'] > 0:
                items = response['Items']
                app.logger.debug(items)
                app.logger.info("get_church_info succeeded:")
                app.logger.info(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))
            else:
                app.logger.info("get_church_info 교회 정보 없음")
        return items


    """
    교회ID로 교회명 조회
    """
    @staticmethod
    def get_church_name( church_id ):

        table = dynamodb.Table(churchTable)
        items = {}
        try:
            response = table.get_item(
                Key={
                    'church_id': church_id
                }
                , ProjectionExpression="church_id, church_name, zip_code, address, address_detail"
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            if 'Item' in response:
                item = response['Item']
                app.logger.info("get_church_name succeeded:")
                app.logger.debug(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))
                app.logger.debug(jsonify(response))
            else:
                print("get_church_name 사용자 정보 없음")

        return item


    """
    교회명 조회
    """
    @staticmethod
    def get_church_name_list( church_name ):

        table = dynamodb.Table(churchTable)
        items = {}
        limit = 50  # 셀갱신시 나중에 처리
        # 패이징 조건 셋
        # if 'esk_church_id' in request.values and request.values['esk_church_id']:
        #     esk = {'church_id': request.values['esk_church_id'], 'worship_date':request.values['esk_worship_date']}

        try:
            # if esk:
            #     response = table.scan(
            #         FilterExpression=Attr('church_name').contains(church_name)
            #         , Limit=limit
            #         , ExclusiveStartKey=esk
            #     )
            # else:
            response = table.scan(
                FilterExpression=Attr('church_name').contains(church_name)
                , Limit=limit
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            if response['Count'] > 0:
                items = response['Items']
                app.logger.debug(items)
                app.logger.debug("get_church_name_list succeeded:")
                app.logger.debug(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))
            else:
                app.logger.info("get_church_name_list 교회 정보 없음")
        return items


"""
교회 id 생성 우편번호+_+yyyymmddhhmmss 22자 등
"""
def create_church_id(zipcode):
    now = datetime.datetime.now()
    return str(request.values['zip_code']) + "_" + str(now.strftime('%Y%m%d%H%M%S'))