#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
#import app
from flask import Flask, redirect, url_for, session

from app import app

@app.route('/')
def go_index():
    #if 'USER_INFO' in session:
    if 'USER_INFO' in session :
        if session['USER_INFO']['SIGNIN_YN'] == 'Y':
            return redirect(url_for('managerWeeklyPaper'))

    return redirect(url_for('go_login'))


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does nota exist', 404