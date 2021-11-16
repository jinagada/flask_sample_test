import logging
import os
import sqlite3
from datetime import timedelta
from pathlib import Path

from flask import Flask, g
from flask_bootstrap import Bootstrap

from services.Sqlite3Serivce import Sqlite3Service
from utils.LogUtil import err_log
from views.LoginView import login
from views.MainView import main

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
app.permanent_session_lifetime = timedelta(minutes=1)
# Blueprint 설정
app.register_blueprint(main)
app.register_blueprint(login)
# Bootstrap 설정
Bootstrap(app)
# env 설정
env_val = None


def get_sqlite3_db():
    """
    Sqlite3 Connection 설정
    :return:
    """
    try:
        result = getattr(g, 'sqlite3', None)
        if result is None:
            db_conn = sqlite3.connect('sample.db')
            db_conn.row_factory = dict_factory
            g.sqlite3 = db_conn
            result = db_conn
    except Exception as e:
        db_conn = sqlite3.connect('sample.db')
        db_conn.row_factory = dict_factory
        result = db_conn
        err_log(logger, e, 'get_sqlite3_db')
    return result


def dict_factory(cursor, row):
    """
    tuple -> dict
    :param cursor:
    :param row:
    :return:
    """
    new_row = {}
    for idx, col in enumerate(cursor.description):
        new_row[col[0]] = row[idx]
    return new_row


@app.before_request
def init_global():
    """
    current_app or g 변수 설정
    before_app_request 가 먼저 호출되고 그 다음 before_request 가 호출됨
    before_app_request 는 Blueprint 에만 존재함
    """
    pass


@app.teardown_appcontext
def close_connection(exception):
    """
    Sqlite3 Connection Close 설정
    :param exception:
    :return:
    """
    if 'sqlite3' in g and g.sqlite3 is not None:
        g.sqlite3.close()


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
    Sqlite3Service(get_sqlite3_db())
