import logging
from datetime import datetime, timedelta

from flask import Blueprint, request, render_template, current_app


main = Blueprint('main', __name__, url_prefix='/')
vw_main_logger = logging.getLogger('flask_sample_test.main')


@main.route('/')
def index():
    """
    Sample Index Page
    :return:
    """
    return render_template('main/index.html')
