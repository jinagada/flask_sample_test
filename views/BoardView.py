import logging
import traceback

from flask import Blueprint, request, g, render_template, jsonify

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
    else:
        board_info = None
    return render_template('board/board_form.html', page_num=page_num, row_per_page=row_per_page, board_info=board_info)


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
        BoardService().save_board(board_seq, title, contents, g.user_info['USER_ID'])
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
    return render_template('board/board_detail.html', page_num=page_num, row_per_page=row_per_page, board_info=board_info)


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
