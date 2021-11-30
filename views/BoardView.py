import logging
import os
import traceback
import uuid

from flask import Blueprint, request, g, render_template, jsonify

from config.Config import PathConfig
from services.BoardService import BoardService
from utils.LogUtil import err_log
from utils.PageUtil import calculate_page
from views.LoginView import login_required, admin_login_required

board = Blueprint('board', __name__, url_prefix='/board')
vw_board_logger = logging.getLogger('flask_sample_test.views.BoardView')


@board.route('/boardList', methods=['GET', 'POST'])
@login_required(is_next=True)
def board_list():
    """
    게시글 목록
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
    board_data_list, totalcount = BoardService().get_board_list((page_num - 1) * row_per_page, row_per_page)
    # 페이징 처리
    block_start, block_end, last_page_num = calculate_page(page_num, row_per_page, totalcount, 5)
    return render_template('board/board_list.html', board_list=board_data_list, page_num=page_num, row_per_page=row_per_page,
                           block_start=block_start, block_end=block_end, last_page_num=last_page_num, totalcount=totalcount)


@board.route('/insertBoardForm', methods=['GET', 'POST'])
@login_required()
def insert_board_form():
    """
    게시글 등록/수정 화면
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
    board_seq = params.get('board_seq')
    if board_seq:
        board_info = BoardService().get_board_by_seq(board_seq)
        if board_info is None:
            raise Exception('게시물이 없습니다.')
        file_list = BoardService().get_board_file_list(board_seq)
    else:
        board_info = None
        file_list = None
    return render_template('board/board_form.html', page_num=page_num, row_per_page=row_per_page, board_info=board_info, file_list=file_list)


@board.route('/saveBoard', methods=['POST'])
@login_required(is_json=True)
def save_board():
    """
    게시글 등록/수정
    :return:
    """
    try:
        # 파라메터 처리
        params = request.form
        title = params.get('title')
        contents = params.get('contents')
        board_seq = params.get('board_seq')
        tmp_seq = BoardService().save_board(board_seq, title, contents, g.user_info['USER_ID'])
        # 첨부파일 처리
        file_seqs = params.getlist('file_seqs')
        file_org_names = params.getlist('file_org_names')
        file_tmp_names = params.getlist('file_tmp_names')
        file_tmp_paths = params.getlist('file_tmp_paths')
        BoardService().save_board_file(tmp_seq if not board_seq else board_seq, file_seqs, file_org_names, file_tmp_names, file_tmp_paths, g.user_info['USER_ID'])
        result = {'is_success': True}
    except Exception as e:
        err_log(vw_board_logger, e, 'BoardView.save_board', traceback.format_exc())
        result = {'is_success': False}
    return jsonify(result)


@board.route('/getBoard', methods=['POST'])
@login_required()
def board_detail():
    """
    게시글 상세보기
    :return:
    """
    # 파라메터 처리
    params = request.form
    # page 파라메터
    page_num = int(params.get('page_num', 1))
    row_per_page = int(params.get('row_per_page', 10))
    board_seq = int(params.get('board_seq', 0))
    board_info = BoardService().get_board_by_seq(board_seq)
    if board_info is None:
        raise Exception('게시물이 없습니다.')
    file_list = BoardService().get_board_file_list(board_seq)
    return render_template('board/board_detail.html', page_num=page_num, row_per_page=row_per_page, board_info=board_info, file_list=file_list)


@board.route('/deleteBoards', methods=['POST'])
@login_required(is_json=True)
@admin_login_required(is_json=True)
def delete_boards():
    """
    게시글 삭제
    :return:
    """
    try:
        # 파라메터 처리
        params = request.form
        board_seq_list = params.getlist('board_seqs')
        BoardService().delete_boards(board_seq_list)
        result = {'is_success': True}
    except Exception as e:
        err_log(vw_board_logger, e, 'BoardView.delete_boards', traceback.format_exc())
        result = {'is_success': False, 'error_msg': str(e)}
    return jsonify(result)


@board.route('', methods=['POST'])
@login_required(is_json=True)
def upload_file():
    """
    파일 업로드 처리
    :return:
    """
    try:
        # 파라메터 처리
        attach_file = request.files['attach_file']
        # 원본파일명
        filename = attach_file.filename
        # 임시저장 디렉토리 설정
        file_tmp_path = PathConfig[g.env_val]['file_tmp_path']
        file_full_path = PathConfig[g.env_val]['file_upload_home'] + os.path.sep + file_tmp_path
        os.makedirs(file_full_path, exist_ok=True)
        # 임시파일명
        file_ext = filename.split('.')[(len(filename.split('.')) - 1)] if len(filename.split('.')) > 1 else ''
        file_tmp_name = str(uuid.uuid4().hex) + '.' + file_ext
        # 업로드 파일 임시저장
        attach_file.save(os.path.join(file_full_path, file_tmp_name))
        result = {'is_success': True, 'file_org_name': filename, 'file_tmp_path': file_tmp_path, 'file_tmp_name': file_tmp_name}
    except Exception as e:
        err_log(vw_board_logger, e, 'BoardView.upload_file', traceback.format_exc())
        result = {'is_success': False, 'error_msg': str(e)}
    return jsonify(result)
