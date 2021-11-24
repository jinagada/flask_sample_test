import logging
import traceback
from datetime import datetime

from flask import Blueprint, request, render_template, jsonify

from services.UsersService import UsersService
from utils.LogUtil import err_log
from utils.PageUtil import calculate_page
from views.LoginView import login_required, admin_login_required

user = Blueprint('user', __name__, url_prefix='/user')
vw_member_logger = logging.getLogger('flask_sample_test.views.UserView')


@user.app_template_filter('formatdtuser')
def _format_datetime(value, format_str='%Y-%m-%d %H:%M:%S'):
    if type(value) is str:
        if value[-1] != 'Z':
            if len(value) == 14:
                result = datetime.strptime(value, '%Y%m%d%H%M%S').strftime(format_str)
            elif len(value) == 19:
                if value.find('T') == -1:
                    result = datetime.strptime(value, '%Y-%m-%d %H:%M:%S').strftime(format_str)
                else:
                    result = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S').strftime(format_str)
            else:
                result = datetime.fromisoformat(value[:-2]).strftime(format_str)
        else:
            result = datetime.fromisoformat(value[:-1]).strftime(format_str)
    elif type(value) is datetime:
        result = value.strftime(format_str)
    else:
        result = ''
    return result


@user.route('/userList', methods=['GET', 'POST'])
@login_required(is_next=True)
@admin_login_required()
def user_list():
    """
    사용자 목록
    :return:
    """
    # 파라메터 처리
    if request.method == 'GET':
        params = request.args
    else:
        params = request.form
    # page 파라메터
    page_num = int(params.get('page_num', 1))
    row_per_page = int(params.get('row_per_page', 10))
    # 목록 조회
    user_data_list, totalcount = UsersService().get_user_list((page_num - 1) * row_per_page, row_per_page)
    # 페이징 처리
    block_start, block_end, last_page_num = calculate_page(page_num, row_per_page, totalcount, 5)
    return render_template('user/user_list.html', user_list=user_data_list, page_num=page_num, row_per_page=row_per_page,
                           block_start=block_start, block_end=block_end, last_page_num=last_page_num, totalcount=totalcount)


@user.route('/saveUser', methods=['POST'])
@login_required(is_json=True)
@admin_login_required(is_json=True)
def save_user():
    """
    사용자 정보 등록/수정
    :return:
    """
    try:
        # 파라메터 처리
        params = request.form
        user_id = params.get('user_id')
        user_pw = params.get('user_pw')
        user_name = params.get('user_name')
        user_seq = params.get('user_seq')
        UsersService().save_user(user_id, user_pw, user_name, user_seq)
        result = {'is_success': True}
    except Exception as e:
        err_log(vw_member_logger, e, 'UserView.save_user', traceback.format_exc())
        result = {'is_success': False}
    return jsonify(result)


@user.route('/getUser', methods=['POST'])
@login_required(is_json=True)
@admin_login_required(is_json=True)
def get_user():
    """
    사용자정보 조회
    :return:
    """
    try:
        # 파라메터 처리
        params = request.form
        user_seq = params.get('user_seq')
        user_info = UsersService().get_user_by_seq(user_seq)
        if user_info is None:
            raise Exception('User Not Found.')
    except Exception as e:
        err_log(vw_member_logger, e, 'UserView.get_user', traceback.format_exc())
        raise e
    return render_template('user/_save_user_modal.html', user_info=user_info)


@user.route('/deleteUsers', methods=['POST'])
@login_required(is_json=True)
@admin_login_required(is_json=True)
def delete_users():
    """
    사용자 삭제
    :return:
    """
    try:
        # 파라메터 처리
        params = request.form
        user_seq_list = params.getlist('user_seqs')
        UsersService().check_delete_users(user_seq_list)
        result = {'is_success': True}
    except Exception as e:
        err_log(vw_member_logger, e, 'UserView.delete_users', traceback.format_exc())
        result = {'is_success': False, 'error_msg': str(e)}
    return jsonify(result)
