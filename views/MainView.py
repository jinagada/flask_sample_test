import logging

from flask import Blueprint, g, render_template

main = Blueprint('main', __name__, url_prefix='/')
vw_main_logger = logging.getLogger('flask_sample_test.views.MainView')


@main.route('/')
def index():
    """
    Sample Index Page
    :return:
    """
    # Login 정보 g 객체에서 확인
    if 'user_info' in g:
        user_info = g.user_info
    else:
        user_info = None
    return render_template('main/index.html', user_info=user_info)
