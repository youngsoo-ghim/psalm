#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
from flask import Flask, redirect, render_template, request, jsonify, \
    url_for, session

from app import app
from app.models.user.user import User
from app.models.church.church import Church
from app.models.weekly import Weekly

weekly = Weekly()

@app.route('/weekly', methods=['GET','POST'])
def go_weekly_paper():
    items = weekly.get_weekly_paper(session)
    return render_template('weekly/weekly_paper.html', items=items).encode('utf-8')
