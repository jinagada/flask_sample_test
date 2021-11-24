import logging
from functools import wraps

from flask import Blueprint, request, session, g, render_template, redirect, url_for, jsonify

from models.LoginModel import LoginModel
from services.UsersService import UsersService

login = Blueprint('login', __name__, url_prefix='/')
vw_login_logger = logging.getLogger('flask_sample_test.views.LoginView')


def login_required(is_next=False, is_json=False):
    """
    Login이 필요한 화면 접근 제어
    :param is_next:
    :param is_json:
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'USER_INFO' not in session:
                if is_next:
                    return redirect(url_for('login.login_form', next=request.url))
                else:
                    if is_json:
                        return jsonify({'error': 403, 'error_msg': url_for('login.login_form')}), 403
                    else:
                        return redirect(url_for('login.login_form'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_login_required(is_json=False):
    """
    Login 이후 관리자 권한이 필요한 경우 제어
    :param is_json:
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session['USER_INFO']['user_id'] != 'admin':
                if is_json:
                    return jsonify({'error': 401, 'error_msg': 'Unauthorized'}), 401
                else:
                    return render_template('error/401.html'), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator


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
    # 파라메터 처리
    if request.method == 'GET':
        params = request.args
    else:
        params = request.form
    next_url = params.get('next', '')
    login_error = params.get('login_error', False)
    return render_template('login/login_form.html', login_error=login_error, next_url=next_url)


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
    next_url = params.get('next_url', '')
    user_info = UsersService().get_user_by_id(user_id)
    if user_info and user_info['USER_PW'] == user_pw:
        # Login session 처리
        session.permanent = True
        session['USER_INFO'] = LoginModel(user_id, user_info['USER_NAME'])
        UsersService().update_login_mdate(user_id)
        if next_url:
            result_url = redirect(next_url)
        else:
            result_url = redirect(url_for('main.index'))
    else:
        result_url = redirect(url_for('login.login_form', login_error=True))
    return result_url


@login.route('/logout')
def logout():
    """
    Logout Process
    :return:
    """
    # session 전체 clear
    session.clear()
    return redirect(url_for('main.index'))
