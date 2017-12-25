#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
from flask import Flask, redirect, render_template, request, jsonify, \
    url_for, session, abort, make_response

from app import app, auth
from app.models.user.user import User
from app.models.church.church import Church, create_church_id


"""
route method 등록시 접두어로 "go_" 을 사용하여 페이지 이동을 처리 하며(GET 처리),
접두어로 "do_" 를 사용하면 해당 정보의 등록, 변경 처리를 하는 것으로 하며
접두어로 "ajax_" 는ajax 처리롤 사용
"""

# User 클래스 인스턴스 생성
#user = User()

# Church 클래스 인스턴스 생성(클래스 메소드 호출 테스트 롤 Chruch 에서 클래스 메소드 선언 self 필효함
#church = Church( request )

"""
로그인을 위한 페이지
"""
@app.route('/login', methods=['GET', 'POST'])
def go_login(result=None):
    #request.__setitem__(request, "name", name)
    #return render_template('customer/signin.html', name=name)
    app.logger.debug(app.template_folder)
    app.logger.debug(app.jinja_loader)
    return render_template('user/logIn.html', result=result )

@app.route('/user/info', methods=['GET'])
def go_reg_user():
    # 사용자 정보는 세션에 있고 교회 정보만 조회
    if 'USER_INFO' in session:
        if session['USER_INFO']['SIGNIN_YN'] == 'Y':
            pass

    return render_template('user/user_info.html')

"""
사용자 정보 등록
"""
@app.route('/user/info', methods=['POST'])
def do_reg_user():
    app.logger.debug(request)
    # 교회에 해당 아이디를 생서 우편번호화 생성 일자 결합
    #church_id = createChurchId(request.values['zip_code']);

    # 입력반응 사용자 정보 저장
    user = User(request)
    user.insert_user_info()
    # 입력 받은 교회 정보 저장
    #regChruchInfo(request, church_id)
    return render_template('user/welcome.html')
    #return jsonify({'status': 'OK'})


"""
사용자 정보 수정
"""
@app.route('/user/<account_email>', methods=['POST'])
#@auth.login_required
def do_update_user(account_email=None):
    app.logger.debug(request)

    church = Church(request)
    #account_email = account_email
    #account_email = session['USER_INFO']['ACCOUNT_EMAIL']

    # 등록 되어있는 교회 정보가 없는 경우 처리
    if request.form['new_yn'] == "Y":

        # 교회에 해당 아이디를 생서 우편번호화 생성 일자 결합
        church_id = create_church_id(request.values['zip_code']);
        #request['church_id'] = church_id

        # 입력반응 사용자 정보 저장
        User.update_user_info(request, account_email, church_id)

        # 입력 받은 교회 정보 저장
        church.insert_chruch(church_id)

    # 등록 되어 있는 교회 정보가 있는 경우 처리
    else:
        User.update_user_info(request, account_email, request.values['church_id'])

    return redirect(url_for('go_weekly_paper'))


"""
사용자 확인
"""
@app.route('/user/id', methods=['POST'])
def ajax_check_user():
    app.logger.debug(request)
    item = User.get_user(request)
    result = ""
    if item:
        result = 'NOTOK'
    else:
        result = 'OK'
    #return json.dumps({'status':'OK'})
    return jsonify({'status': result})

"""
로그인 처리
"""
@app.route('/user/login', methods=['POST'])
@auth.verify_password
def do_login():
    app.logger.debug(request)
    # if request.method == 'POST':
    #     resulta = request.form['account_email']

    item = User.do_login(request)
    result = ''
    if item:
        result = 'OK'
        #
        if item['account_email'] == request.form['account_email']:
            session.clear()
            session['USER_INFO'] = {}
            session['USER_INFO']['SIGNIN_YN'] = 'Y'
            session['USER_INFO']['ACCOUNT_EMAIL'] = item['account_email']
            session['USER_INFO']['LASTNAME'] = item['lastname']
            session['USER_INFO']['FIRSTNAME'] = item['firstname']
            # 최초 가입자는 교회정보가 없음
            if 'church_id' in item:
                session['USER_INFO']['CHURCH_ID'] = item['church_id']
            else:
                # 교회 정보 없을 경우 교회 정보 등로 하는 화면 이동
                session['USER_INFO']['CHURCH_ID'] = ''
                return redirect(url_for('go_church_info'))

            #session['USER_INFO']['CHURCH_NAME'] = item['church_name']
            #print(url_for('regId', regId='regId'))
            #return redirect(url_for('userregId'))
            return redirect(url_for('go_weekly_paper'))
        else:
            abort(400)
            #result = 'DANGER'
            #return redirect(url_for('goLogin', result=result))

    else:
        result = 'NOTOK'
        return redirect(url_for('go_login', result=result))
        #return render_template('user/signIn.html', result=result)


"""
    로그아웃
"""
@app.route('/logout', methods=['GET', 'POST'])
def do_logout():
    session.clear()
    return redirect(url_for('go_index'))


@app.errorhandler(400)
def uncaughtError(error):
    return '잘못된 사용입니다.'


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error':'Unauthorized access'}), 401)