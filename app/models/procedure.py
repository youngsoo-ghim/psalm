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
procedureTable = 'psalm_Procedure'

class Procedure():
    """
        주보 리스트 조회
    """
    @staticmethod
    def list_procedure(session, request):
        table = dynamodb.Table(procedureTable)
        church_id = session['USER_INFO']['CHURCH_ID']
        #weekly_date = session['weekly_date']
        items = None
        # params = { 'KeyConditionExpression':Key('church_id').eq(church_id)
        #             ,'ScanIndexForward':False
        #             ,'Limit':1
        #             ,'ProjectionExpression':'church_id, church_name, worship_name, worship_date, reg_date, update_date'
        #         }
        # if 'worship_name' in request.values and request.values['worship_name']:
        #     params['FilterExpression'] = Attr('worship_name').contains(request.values['worship_name'])
        # if 'esk_church_id' in request.form:
        #     esk = {'church_id': request.form['esk_church_id'], 'worship_date':request.form['esk_worship_date']}
        #     params['ExclusiveStartKey'] = esk

        # 카값 셋
        kce = Key('church_id').eq(church_id)
        pe = 'church_id, church_name, worship_name, worship_date, reg_date, update_date'
        limit = 10
        fe = None
        esk = None
        response = None
        # 검색조선 셋
        if 'worship_name' in request.values and request.values['worship_name']:
            fe = Attr('worship_name').contains(request.values['worship_name'])

        # 패이징 조건 셋
        if 'esk_church_id' in request.values and request.values['esk_church_id']:
            esk = {'church_id': request.values['esk_church_id'], 'worship_date':request.values['esk_worship_date']}

        try:
            # 조회 조건 있음
            if fe:
                # 페이징 처리
                if esk:
                    response = table.query(
                        KeyConditionExpression=kce
                        , ScanIndexForward = False
                        , FilterExpression = fe
                        #,FilterExpression = Attr('worship_name').contains('')
                        #,ExpressionAttributeNames={"#yr": "year"},  # Expression Attribute Names for Projection Expression only.
                        , ProjectionExpression = pe
                        , Limit=limit
                        , ExclusiveStartKey=esk
                    )
                else:
                    response = table.query(
                        KeyConditionExpression=kce
                        , ScanIndexForward = False
                        , FilterExpression = fe
                        , ProjectionExpression = pe
                        , Limit=limit
                    )
            else:
                if esk:
                    response = table.query(
                        KeyConditionExpression=kce
                        , ScanIndexForward = False
                        , ProjectionExpression = pe
                        , Limit=limit
                        , ExclusiveStartKey=esk
                    )
                else:
                    response = table.query(
                        KeyConditionExpression = kce
                        , ScanIndexForward = False
                        , ProjectionExpression = pe
                        , Limit = limit
                    )

        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])

        else:
            if response['Count'] > 0:
                items = response['Items']
                app.logger.debug(type(items))
                app.logger.debug(response['ScannedCount'])
                app.logger.debug(json.dumps(response, indent=2, cls=DecimalEncoder, ensure_ascii=False))
                app.logger.info("list_procedure succeeded:")
            else:
                app.logger.info("get_procedure_list 정보 없음")
        return response


    """
    교회 ID로 주보 리스트 조회
    """
    @staticmethod
    def list_procedure_for_church_id(church_id):
        table = dynamodb.Table(procedureTable)

        items = {}
        try:
            response = table.query(
                KeyConditionExpression=Key('church_id').eq(church_id)
                ,ScanIndexForward = False
                #FilterExpression = Attr('church_name').eq('광림교회')
                #,ExpressionAttributeNames={"#yr": "year"},  # Expression Attribute Names for Projection Expression only.
                ,ProjectionExpression = "church_id, church_name, worship_name, worship_date, reg_date, update_date"
                ,Limit=10
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            if response['Count'] > 0:
                app.logger.debug(type(items))
                items = response['Items']
                app.logger.info("list_procedure_for_id succeeded:")
                app.logger.debug(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))
            else:
                app.logger.info("get_procedure_list 정보 없음")
        return items


    """
    예배 순서 상세 조회
    """
    @staticmethod
    def get_procedure(request):
        table = dynamodb.Table(procedureTable)

        app.logger.debug(session)
        #church_id = session['USER_INFO']['CHURCH_ID']
        church_id = request.form['church_id']
        worship_date = request.form['worship_date']
        #weekly_date = session['weekly_date']
        item = []
        try:
            response = table.get_item(
                Key={
                    'church_id':church_id
                    ,'worship_date':worship_date
                }
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            if 'Item' in response:
                item = response['Item']
                app.logger.info("get_procedure succeeded:")
                app.logger.debug(json.dumps(item, indent=4, cls=DecimalEncoder, ensure_ascii=False))
            else:
                app.logger.info("get_procedure 정보 없음")
        return item


    """
    예배 순서 등록
    """
    @staticmethod
    def insert_worship_procedure( session, request ):
        table = dynamodb.Table(procedureTable)
        #weekly_date = session['weekly_date']
        now = datetime.datetime.now()
        reg_date = now.strftime('%Y-%m-%d %H:%M:%S')

        worship_proceduce_data = []

        procedure = {}
        # 등록된 예배 순서 길이 만큼데이터 처리
        app.logger.info(len(request.form['procedure']))
        for i in request.form.getlist('procedure'):
            dic_1 = {}          # 기본정보 넣을 딕셔너리
            dic_2 = {}          # 링크정보 넣을 딕셔너리

            # request 에서 stand_up 값이 있으면 값 입력
            if request.form.getlist('stand_up_'+str(i)) :
                dic_1['stand_up'] = 'Y'
            # request 에서 title 값이 있으면 값 입력
            if request.form['title_'+str(i)] :
                dic_1['title'] = request.form['title_'+str(i)]
            if request.form['etc_'+str(i)] :
                dic_1['etc'] = request.form['etc_'+str(i)]
            if request.form['contents_'+str(i)] :
                dic_1['contents'] = request.form['contents_'+str(i)]

            # 타입이 dic_2 에 link 인 값 생성
            if request.form['contents_type_'+str(i)] and \
                    request.form['contents_type_'+str(i)] == 'link':

                dic_2['kind'] = request.form['link_type_'+str(i)]

                if request.form['link_to_'+str(i)]:
                    dic_2['link_to'] = request.form['link_to_'+str(i)]

                if request.form['from_bible_'+str(i)]:
                    dic_2['from_bible'] = request.form['from_bible_'+str(i)]
                if request.form['from_chapter_'+str(i)]:
                    dic_2['from_chapter'] = request.form['from_chapter_'+str(i)]
                if request.form['from_paragraph_'+str(i)]:
                    dic_2['from_paragraph'] = request.form['from_paragraph_'+str(i)]

                if request.form['to_bible_'+str(i)]:
                    dic_2['to_bible'] = request.form['to_bible_'+str(i)]
                if request.form['to_chapter_'+str(i)]:
                    dic_2['to_chapter'] = request.form['to_chapter_'+str(i)]
                if request.form['to_paragraph_'+str(i)]:
                    dic_2['to_paragraph'] = request.form['to_paragraph_'+str(i)]

                dic_1['link'] = dic_2

            # 예배 순서 딕셔너리에 생성
            procedure[''+i+''] = dic_1

        try:
            response = table.put_item(
                Item={
                    'church_id': request.form['church_id']
                    , 'worship_date': request.form['worship_date']
                    , 'church_name': request.form['church_name']
                    , 'worship_name': request.form['worship_name']
                    , 'reg_date': reg_date
                    , 'update_date': reg_date
                    , 'change_user_id': session['USER_INFO']['ACCOUNT_EMAIL']
                    , 'worship_procedure' : procedure
                }
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            app.logger.info("insert_worship_procedure succeeded:")
            app.logger.debug(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))

    """
    예배 순서 키로 상세 조회 (church_id, worship_date )
    """
    @staticmethod
    def get_procedure_detail( church_id, worship_date):
        table = dynamodb.Table(procedureTable)
        #church_id = session['USER_INFO']['CHURCH_ID']
        #weekly_date = session['weekly_date']
        item = []
        try:
            response = table.get_item(
                Key={
                    'church_id':church_id
                    ,'worship_date':worship_date
                }
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            if 'Item' in response:
                item = response['Item']
                app.logger.info("get_procedure_detail succeeded:")
                app.logger.debug(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))
            else:
                app.logger.info("get_procedure_detail 정보 없음")
        return item

    """
    예배 순서 삭제
    """
    @staticmethod
    def delete_procedure( request ):
        table = dynamodb.Table(procedureTable)
        church_id = request.form['church_id']
        worship_date = request.form['worship_date']

        try:
            response = table.delete_item(
                Key={
                    'church_id': church_id
                    ,'worship_date': worship_date
                }
            )
        except ClientError as e:
            app.logger.error(e.response['Error']['Message'])
        else:
            app.logger.info("delete_procedure succeeded")
            app.logger.debug(json.dumps(response, indent=4, cls=DecimalEncoder, ensure_ascii=False))
