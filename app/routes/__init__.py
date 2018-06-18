#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
from app import app
from flask import render_template, session
from datetime import timedelta


"""
사용자가 페이지 이동시 세션 사용 시간 갱신 하도록 처리
"""
@app.before_request
def make_session_permanent():
    app.logger.debug(session)
    if 'USER_INFO' in session and session['USER_INFO']['SIGNIN_YN'] == 'Y':
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=20)
        #return render_template('error/sessionTimeout.html')

@app.errorhandler(400)
def uncaughtError(error):
    #return '잘못된 사용입니다.'
    app.logger.error('Server Error: %s', (error))
    return render_template('error/400.html'), 400

# @app.errorhandler(500)
# def uncaughtError(error):
#     return '컴파일 잘못된 사용입니다.'

@app.errorhandler(404)
def page_not_found(error):
    #return 'This page does not exist init', 404
    app.logger.error('Server Error: %s', (error))
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('error/500.html'), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return render_template('error/exception.html'), 500