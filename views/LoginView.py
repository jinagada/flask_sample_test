import logging

from flask import Blueprint, request, session, render_template, redirect, url_for

from model.LoginModel import LoginModel
from service.UsersService import UsersService

login = Blueprint('login', __name__, url_prefix='/')
vw_login_logger = logging.getLogger('flask_sample_test.login')


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
    session['USER_INFO'] = LoginModel(user_id, user_pw)
    UsersService().update_login_mdate(user_id, user_pw, user_id)
    return redirect(url_for('main.index'))


@login.route('/logout')
def logout():
    """
    Logout Process
    :return:
    """
    session.pop('USER_INFO', None)
    return redirect(url_for('main.index'))
