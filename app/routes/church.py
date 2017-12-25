#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
#import app
from app import app
from flask import Flask, redirect, url_for, session, request, jsonify, \
    render_template

from app.models.church.church import Church
from botocore.exceptions import ClientError

"""
교회 정보 등록 페이지 이동
"""
@app.route('/church/info', methods=['GET'])
def go_church_info():
    return render_template('church/church_info.html')


"""
이름으로 검색한 교회 정보 전달
"""
@app.route('/church', methods=['GET'])
def ajax_church_list():
    app.logger.debug(request)

    #church = Church(request)
    items = Church.get_church_info(request)
    result = ""
    # 교회 정보 있는경우
    if items:
        result = 'OK'
    else:
        result = 'NOTOK'

    #return json.dumps({'status':'OK'})
    return jsonify({'items': items, 'status': result})


@app.route('/church/info', methods=['POST'])
def do_reg_church():
    app.logger.debug(request)
    church = Church(request)
    item = church.get_church_info()
    result = ""
    if item:
        result = 'NOTOK'
    else:
        result = 'OK'
    #return json.dumps({'status':'OK'})
    return jsonify({'status': result})


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404