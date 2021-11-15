import logging
import os
from pathlib import Path

from flask import Flask
from flask_bootstrap import Bootstrap

from service.Sqlite3Serivce import Sqlite3UserService, Sqlite3BoardService
from views.LoginView import login
from views.MainView import main

# logging 설정
logger = logging.getLogger('flask_sample_test')

# Flask 설정
app = Flask(__name__)
# session 용 secret_key 설정
app.secret_key = 'flask_sample_test_secret_key'
# Blueprint 설정
app.register_blueprint(main)
app.register_blueprint(login)
# Bootstrap 설정
Bootstrap(app)
# env 설정
env_val = None


@app.before_request
def init_global():
    """
    current_app 변수 설정
    """
    pass


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
    # Sqlite3 설정
    Sqlite3UserService()
    Sqlite3BoardService()
