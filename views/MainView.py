import logging

from flask import Blueprint, session, render_template
from service.UsersService import UsersService

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
        user_info = UsersService().get_user_by_id(session['USER_INFO']['user_id'])
    else:
        user_info = None
    return render_template('main/index.html', user_info=user_info)
