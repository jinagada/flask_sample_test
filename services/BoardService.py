import logging
import traceback

from datasources.Sqlite3 import Sqlite3
from utils.LogUtil import err_log


class BoardService:
    """
    Board 데이터 처리
    """

    def __init__(self):
        """
        Class 생성 및 변수선언
        """
        self.logger = logging.getLogger('flask_sample_test.services.BoardService')

    def get_board_list(self, start_row, row_per_page):
        """
        Board 목록 조회
        :param start_row:
        :param row_per_page:
        :return:
        """
        try:
            board_list = Sqlite3().execute('SELECT SEQ, TITLE, RDATE, RUSER, MDATE, MUSER FROM BOARDS ORDER BY RDATE DESC LIMIT ?, ?', (start_row, row_per_page))
            totalcount = Sqlite3().execute(query='SELECT COUNT(*) AS CNT FROM BOARDS', is_one=True)['CNT']
        except Exception as e:
            err_log(self.logger, e, 'BoardService.get_board_list', traceback.format_exc())
            board_list = None
            totalcount = 0
        return board_list, totalcount

    def get_board_by_seq(self, board_seq):
        """
        Board 정보 조회
        :param board_seq:
        :return:
        """
        try:
            board_info = Sqlite3().execute('SELECT SEQ, TITLE, CONTENTS, RDATE, RUSER, MDATE, MUSER FROM BOARDS WHERE SEQ = ?', (board_seq,), True)
        except Exception as e:
            err_log(self.logger, e, 'BoardService.get_board_by_seq', traceback.format_exc())
            board_info = None
        return board_info

    def insert_board(self, title, contents, user_id):
        """
        Board 정보 등록
        :param title:
        :param contents:
        :param user_id:
        :return:
        """
        try:
            result = Sqlite3().cmd('INSERT INTO BOARDS (TITLE, CONTENTS, RDATE, RUSER, MDATE, MUSER) VALUES (?, ?, DATETIME(\'now\', \'localtime\'), ?, DATETIME(\'now\', \'localtime\'), ?)',
                                   (title, contents, user_id, user_id))
        except Exception as e:
            err_log(self.logger, e, 'BoardService.insert_board', traceback.format_exc())
            result = -1
        return result

    def update_board(self, board_seq, title, contents, user_id):
        """
        Board 정보 수정
        :param board_seq:
        :param title:
        :param contents:
        :param user_id:
        :return:
        """
        try:
            result = Sqlite3().cmd('UPDATE BOARDS SET TITLE = ?, CONTENTS = ?, MUSER = ?, MDATE = DATETIME(\'now\', \'localtime\') WHERE SEQ = ?',
                                   (title, contents, user_id, board_seq))
        except Exception as e:
            err_log(self.logger, e, 'BoardService.update_board', traceback.format_exc())
            result = -1
        return result

    def delete_boards(self, board_seq_list):
        """
        Board 삭제
        :param board_seq_list:
        :return:
        """
        try:
            in_query_str = ','.join(list(''.rjust(len(board_seq_list), '?')))
            result = Sqlite3().cmd(f'DELETE FROM BOARDS WHERE SEQ IN ({in_query_str})', tuple(board_seq_list))
        except Exception as e:
            err_log(self.logger, e, 'BoardService.delete_boards', traceback.format_exc())
            result = -1
        return result

    def save_board(self, board_seq, title, contents, user_id):
        """
        Board 정보 저장
        :param board_seq:
        :param title:
        :param contents:
        :param user_id:
        :return:
        """
        if board_seq:
            board_info = self.get_board_by_seq(board_seq)
        else:
            board_info = None
        if board_info:
            result = self.update_board(board_seq, title, contents, user_id)
        else:
            result = self.insert_board(title, contents, user_id)
        if result != 1:
            raise Exception('Save Board Error')
