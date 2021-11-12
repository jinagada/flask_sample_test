import logging
import os
from pathlib import Path

from flask import Flask, current_app
from flask_bootstrap import Bootstrap

from views.SampleView import main


# logging 설정
logger = logging.getLogger('flask_sample_test')

# Flask 설정
app = Flask(__name__)
# Blueprint 설정
app.register_blueprint(main)
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
