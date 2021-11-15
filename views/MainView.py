import logging
from datetime import datetime, timedelta

from flask import Blueprint, request, session, render_template, current_app


main = Blueprint('main', __name__, url_prefix='/')
vw_main_logger = logging.getLogger('flask_sample_test.main')


@main.route('/')
def index():
    """
    Sample Index Page
    :return:
    """
    # Login 정보 session에서 확인
    if 'USER_INFO' in session:
        user_info = session['USER_INFO']
    else:
        user_info = None
    return render_template('main/index.html', user_info=user_info)
