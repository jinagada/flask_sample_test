import logging
import traceback

from datasources.Sqlite3 import Sqlite3
from utils.LogUtil import err_log


class UsersService:
    """
    Users 데이터 처리
    """

    def __init__(self):
        """
        Class 생성 및 변수선언
        """
        self.logger = logging.getLogger('flask_sample_test.services.UsersService')

    def get_user_by_id(self, user_id):
        """
        User 정보 조회
        :param user_id:
        :return:
        """
        try:
            user_info = Sqlite3().execute('SELECT SEQ, USER_ID, USER_PW, USER_NAME, RDATE, MDATE FROM USERS WHERE USER_ID = ?', (user_id,), True)
        except Exception as e:
            err_log(self.logger, e, 'UsersService.get_user_by_id', traceback.format_exc())
            user_info = None
        return user_info

    def get_user_by_seq(self, user_seq):
        """
        User 정보 조회
        :param user_seq:
        :return:
        """
        try:
            user_info = Sqlite3().execute('SELECT SEQ, USER_ID, USER_PW, USER_NAME, RDATE, MDATE FROM USERS WHERE SEQ = ?', (user_seq,), True)
        except Exception as e:
            err_log(self.logger, e, 'UsersService.get_user_by_seq', traceback.format_exc())
            user_info = None
        return user_info

    def get_user_list(self, start_row, row_per_page):
        """
        User 목록 조회
        :param start_row:
        :param row_per_page:
        :return:
        """
        try:
            user_list = Sqlite3().execute('SELECT SEQ, USER_ID, USER_PW, USER_NAME, RDATE, MDATE FROM USERS ORDER BY RDATE DESC LIMIT ?, ?', (start_row, row_per_page))
            totalcount = Sqlite3().execute(query='SELECT COUNT(*) AS CNT FROM USERS', is_one=True)['CNT']
        except Exception as e:
            err_log(self.logger, e, 'UsersService.get_user_list', traceback.format_exc())
            user_list = None
            totalcount = 0
        return user_list, totalcount

    def insert_user(self, user_id, user_pw, user_name):
        """
        User 정보 등록
        :param user_id:
        :param user_pw:
        :param user_name:
        :return:
        """
        try:
            result = Sqlite3().cmd('INSERT INTO USERS (USER_ID, USER_PW, USER_NAME, RDATE, MDATE) VALUES (?, ?, ?, DATETIME(\'now\', \'localtime\'), DATETIME(\'now\', \'localtime\'))',
                          (user_id, user_pw, user_name))
        except Exception as e:
            err_log(self.logger, e, 'UsersService.insert_user', traceback.format_exc())
            result = -1
        return result

    def update_mdate(self, user_id):
        """
        수정일 변경
        :return:
        """
        try:
            result = Sqlite3().cmd('UPDATE USERS SET MDATE = DATETIME(\'now\', \'localtime\') WHERE USER_ID = ?', (user_id,))
        except Exception as e:
            err_log(self.logger, e, 'UsersService.update_mdate', traceback.format_exc())
            result = -1
        return result

    def update_login_mdate(self, user_id):
        """
        로그인 처리 및 최종 로그인일 변경
        :param user_id:
        """
        if self.get_user_by_id(user_id):
            self.update_mdate(user_id)

    def update_user(self, user_seq, user_id, user_pw, user_name):
        """
        User 정보 수정
        :param user_seq:
        :param user_id:
        :param user_pw:
        :param user_name:
        :return:
        """
        try:
            result = Sqlite3().cmd('UPDATE USERS SET USER_ID = ?, USER_PW = ?, USER_NAME = ?, MDATE = DATETIME(\'now\', \'localtime\') WHERE SEQ = ?',
                          (user_id, user_pw, user_name, user_seq))
        except Exception as e:
            err_log(self.logger, e, 'UsersService.insert_user', traceback.format_exc())
            result = -1
        return result

    def save_user(self, user_id, user_pw, user_name, user_seq):
        """
        User 정보 저장
        :param user_id:
        :param user_pw:
        :param user_name:
        :param user_seq:
        :return:
        """
        if user_seq:
            user_info = self.get_user_by_seq(user_seq)
        else:
            user_info = None
        if user_info:
            result = self.update_user(user_seq, user_id, user_pw, user_name)
        else:
            result = self.insert_user(user_id, user_pw, user_name)
        if result != 1:
            raise Exception('Save User Error')
