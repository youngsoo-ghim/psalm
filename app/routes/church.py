#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
#import app
from app import app
from flask import Flask, redirect, url_for, session, request, jsonify, \
    render_template

from app.models.church.church import Church, create_church_id
from botocore.exceptions import ClientError

"""
교회 정보 등록 페이지 이동
"""
@app.route('/church/info', methods=['GET', 'POST'])
def go_church_info():
    if request.method == 'GET' and request.values['change'] == 'Y':
        return render_template('church/church_info.html', change='Y')
    else:
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


@app.route('/church/u', methods=['POST'])
def do_reg_church():
    church = Church(request)
    if request.form['new_yn'] == "Y":
    # 교회에 해당 아이디를 생서 우편번호화 생성 일자 결합
        church_id = create_church_id(request.values['zip_code']);
    # request['church_id'] = church_id

    # 입력 받은 교회 정보 저장
        church.insert_chruch(church_id, session)
    else:
        church.update_church_info(request, session)

    return render_template('church/church_info.html', change='Y')


# @app.errorhandler(404)
# def page_not_found(error):
#     return 'This page does not existchurcch', 404

"""
REST 이름으로 검색한 교회 정보 전달
"""
@app.route('/church/<church_name>', methods=['GET'])
def get_church_list( church_name ):

    items = Church.get_church_name_list(church_name)
    result = ""
    # 교회 정보 있는경우
    if items:
        result = 'OK'
    else:
        result = 'NOTOK'

    #return json.dumps({'status':'OK'})
    return jsonify({'items': items, 'status': result})
    #return jsonify({'items':items})