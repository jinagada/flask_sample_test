import logging
from datetime import datetime, timedelta

from flask import Blueprint, request, session, render_template, current_app, redirect, url_for
from model.LoginModel import LoginModel


login = Blueprint('login', __name__, url_prefix='/')
vw_main_logger = logging.getLogger('flask_sample_test.login')


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
    session['USER_INFO'] = LoginModel(params.get('user_id', ''), params.get('user_pw', ''))
    return redirect(url_for('main.index'))


@login.route('/logout')
def logout():
    """
    Logout Process
    :return:
    """
    session.pop('USER_INFO', None)
    return redirect(url_for('main.index'))
