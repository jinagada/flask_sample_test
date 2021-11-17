import logging

from flask import Blueprint, request, session, g, render_template, redirect, url_for

from models.LoginModel import LoginModel
from services.UsersService import UsersService

login = Blueprint('login', __name__, url_prefix='/')
vw_login_logger = logging.getLogger('flask_sample_test.login')


@login.before_app_request
def load_login_user_info():
    """
    session 에서 로그인 ID 확인 후 사용자 정보를 조회하여 g 객체에 담는다.
    g 객체에 저장된 데이터의 scope은 request 이다.
    before_request : 설정한 Blueprint 내에서만 동작
    before_app_request : App 전체에서 동작
    :return:
    """
    if 'USER_INFO' in session:
        if 'user_info' not in g:
            user_info = UsersService().get_user_by_id(session['USER_INFO']['user_id'])
            g.user_info = user_info
    else:
        g.user_info = None


@login.route('/loginForm')
def login_form():
    """
    Sample Login Form Page
    :return:
    """
    return render_template('login/login_form.html')


@login.route('/loginProcess', methods=['GET', 'POST'])
def login_process():
    """
    Login Process
    :return:
    """
    # 파라메터 처리
    if request.method == 'GET':
        params = request.args
    else:
        params = request.form
    user_id = params.get('user_id', '')
    user_pw = params.get('user_pw', '')
    # Login session 처리
    session.permanent = True
    session['USER_INFO'] = LoginModel(user_id, user_pw)
    UsersService().update_login_mdate(user_id, user_pw, user_id)
    return redirect(url_for('main.index'))


@login.route('/logout')
def logout():
    """
    Logout Process
    :return:
    """
    # session 전체 clear
    session.clear()
    return redirect(url_for('main.index'))
