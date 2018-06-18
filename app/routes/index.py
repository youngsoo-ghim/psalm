#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
#import app
from flask import Flask, redirect, url_for, session,render_template

from app import app

import xlsxwriter
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

@app.route('/')
def go_index():
    if 'USER_INFO' in session :
        if session['USER_INFO']['SIGNIN_YN'] == 'Y':
            return redirect(url_for('go_procedure_list'))
    return redirect(url_for('go_login'))

"""
데이터 작업용 text 자료 정렬 하여 엑셀로 저장
"""
def text_to_excel():
    f = open("/Users/ghim/Documents/문서/작업/찬송가/221.txt", 'r')
    #with open('/Users/ghim/Documents/문서/작업/찬송가/221.txt', 'r', encoding="utf-8") as f:
    #lines = f.readlines()

    workbook = xlsxwriter.Workbook('/Users/ghim/Documents/문서/작업/찬송가/Expenses01.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    lyric = ''
    #for i in range(0, 11079)
    while True:
        line = f.readline()
        app.logger.debug("row :"+str(row))

        if ". " in line:
            app.logger.debug("line : "+line)
            app.logger.debug("value1 : "+line.split('. ')[0].strip())
            app.logger.debug("value1 : "+line.split('. ')[1].strip())
            worksheet.write(row, 0, line.split('. ')[0].strip())
            worksheet.write(row, 1, line.split('. ')[1].strip())
            row = row + 1
            if lyric:
                app.logger.debug(lyric.strip())
                worksheet.write(row-2, 2, lyric.strip())
                lyric = ''
        else:
            lyric = lyric + line

        if not line: break
            #app.logger.debug(lyric)


        #app.logger.debug(i)

    workbook.close()
    f.close()


@app.route('/test')
def go_indexddd():
    # if 'USER_INFO' in session :
    #     if session['USER_INFO']['SIGNIN_YN'] == 'Y':
    #         return redirect(url_for('go_procedure_list'))
    # return redirect(url_for('go_login'))
    return render_template('abcweb.html')

# @app.errorhandler(404)
# def page_not_found(error):
#     return 'This page does nota exist index', 404