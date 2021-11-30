import logging
import os
from datetime import timedelta
from pathlib import Path

from flask import Flask, g, render_template
from flask_bootstrap import Bootstrap

from services.Sqlite3Serivce import Sqlite3Service
from views.BoardView import board
from views.LoginView import login
from views.MainView import main
from views.UserView import user

# logging 설정
logger = logging.getLogger('flask_sample_test')

# Flask 설정
app = Flask(__name__)
# session 설정
"""
import secrets

key = secrets.token_hex(16)
print(key)
"""
app.secret_key = 'cf7f5046e2f3b85087a1d388fb8bec62'
app.permanent_session_lifetime = timedelta(minutes=5)
# 파일업로드 크기 설정(2MB)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000
# Blueprint 설정
app.register_blueprint(main)
app.register_blueprint(login)
app.register_blueprint(user)
app.register_blueprint(board)
# Bootstrap 설정
Bootstrap(app)
# env 설정
env_val = None


@app.before_request
def init_global():
    """
    current_app or g 변수 설정
    before_app_request 가 먼저 호출되고 그 다음 before_request 가 호출됨
    before_app_request 는 Blueprint 에만 존재함
    """
    if 'env_val' not in g:
        g.env_val = env_val


@app.errorhandler(404)
def page_not_found(error):
    """
    404 Error 화면
    주요 Error 화면 처리는 Blueprint 에서 처리가 안되는 듯 보임
    :param error:
    :return:
    """
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    500 Error 화면
    주요 Error 화면 처리는 Blueprint 에서 처리가 안되는 듯 보임
    :param error:
    :return:
    """
    return render_template('error/500.html', error_msg=error.original_exception), 500


def init(env):
    """
    Logger 및 각종 환경설정
    :param env:
    """
    # env별 설정
    global env_val
    if env == 'local':
        home = str(Path(os.path.expanduser('~')))
        log_path = home + '/logs/flask_sample_test'
    else:
        home = str(Path(os.path.expanduser('~')))
        log_path = home + '/logs/flask_sample_test'
    env_val = env
    # Log 디렉토리 생성
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    # Logger 설정
    formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] %(filename)s(%(lineno)d) : %(message)s')
    file_handler = logging.FileHandler(log_path + os.sep + 'flask_sample_test.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if env == 'local':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    # Sqlite3 초기 테이블 설정
    Sqlite3Service()
