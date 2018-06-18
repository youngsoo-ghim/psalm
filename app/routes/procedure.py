#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
from flask import Flask, redirect, render_template, request, jsonify, \
    url_for, session, abort
from werkzeug.debug import get_current_traceback
from datetime import datetime

from app import app
from app.models.user.user import User
from app.models.church.church import Church
from app.models.procedure import Procedure

procedure = Procedure()

"""
예배순서리스트
"""
@app.route('/procedure', methods=['GET'])
def go_procedure_list():
    try:
        response = procedure.list_procedure(session, request)
        items = response['Items']
        # 마지막 값을 가지고 있으면 다음 조회 가능 하도록 하고 없으면 없는 값 셋
        if 'LastEvaluatedKey' in response:
            esk_worship_date = response['LastEvaluatedKey']['worship_date']
            esk_church_id = response['LastEvaluatedKey']['church_id']
        else:
            esk_worship_date = None
            esk_church_id = None

    except Exception as e:
        #app.logger.error(e)
        track = get_current_traceback(skip=1, show_hidden_frames=True,
                                      ignore_system_exceptions=False)
        app.logger.error(track.log())
    return render_template('procedure/procedure_list.html', items=items, esk_worship_date=esk_worship_date, esk_church_id=esk_church_id).encode('utf-8')


"""
REST 예배순서리스트
"""
@app.route('/procedurelist', methods=['GET'])
def rest_go_procedure_list_continue():
    try:
        response = procedure.list_procedure(session, request)
        if response:
            items = response['Items']
            # 마지막 값을 가지고 있으면 다음 조회 가능 하도록 하고 없으면 없는 값 셋
            if 'LastEvaluatedKey' in response:
                esk_worship_date = response['LastEvaluatedKey']['worship_date']
                esk_church_id = response['LastEvaluatedKey']['church_id']
            else:
                esk_worship_date = None
                esk_church_id = None
            return jsonify({'items': items, 'esk_worship_date':esk_worship_date, 'esk_church_id':esk_church_id})
        else:
            return jsonify({'items': None, 'esk_worship_date':None, 'esk_church_id':None})
    except Exception as e:
        #app.logger.error(e)
        track = get_current_traceback(skip=1, show_hidden_frames=True,
                                      ignore_system_exceptions=False)
        app.logger.error(track.log())
    return jsonify({'items': None, 'esk_worship_date':None, 'esk_church_id':None})

"""
예배순서 상세
"""
@app.route('/procedure', methods=['POST'])
def go_procedure():
    if request.form['worship_date']:
        item = procedure.get_procedure(request)
        return render_template('procedure/procedure.html', item=item)
    else:
        return render_template('procedure/procedure.html', item=None)


"""
REST API 예배순서리스트 json return
"""
@app.route('/procedure/<church_id>', methods=['GET'])
def rest_go_procedure_list(church_id):
    items = procedure.list_procedure_for_church_id(church_id)
    return jsonify({'items': items})


"""
REST API 예배순서 상세
"""
@app.route('/procedure/<church_id>/<worship_date>', methods=['GET'])
def rest_go_procedure(church_id, worship_date):
    items = procedure.get_procedure_detail(church_id, worship_date)
    return jsonify({'items': items})


"""
예배순서 등록
"""
@app.route('/worship/procedure', methods=['POST'])
def do_reg_procedure():
    procedure.insert_worship_procedure( session, request )
    return redirect(url_for('go_procedure_list'))


# @app.template_filter('dt')
# def _jinja2_filter_datetime(date, fmt=None):
#     if fmt:
#         return date.strftime(fmt)
#     else:
#         return date.strftime(gettext('%%m/%%d/%%Y'))

"""
예배 순서 삭제
"""
@app.route('/worship/procedure/delete', methods=['POST'])
def do_delete_procedure():
    procedure.delete_procedure( request )
    return redirect(url_for('go_procedure_list'))


"""
jinja filter data 형태 값을 표현
"""
@app.template_filter('datetimeformat')
def _jinja2_filter_datetime(value, format=None):
    if value:
        if format:
            return datetime.strptime(value, format)
        else:
            return datetime.strptime(value, '%Y%m%d%H%M%S')
    else:
        return


#app.jinja_env.filters['datetimeformat'] = _jinja2_filter_datetime
