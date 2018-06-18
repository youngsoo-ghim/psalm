#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
#import app
import os
from flask import jsonify, render_template, request

from app import app


"""
REST 새찬송가 번호로 조회
"""
@app.route('/score/<number>', methods=['GET'])
def rest_hymn_number(number):
    f = open(os.path.join('templates') + "/score/score_data/" + number +".abc", 'r')
    #lines = f.readlines()
    content = f.read()
    return render_template('score/score.html', score_number=number, content=content)