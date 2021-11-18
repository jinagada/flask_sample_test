import logging
import traceback
from datetime import datetime

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
        self.logger = logging.getLogger('flask_sample_test.UsersService')

    def get_user_by_id(self, user_id):
        """
        User 정보 조회
        :param user_id:
        :return:
        """
        try:
            user_info = Sqlite3().execute('SELECT USER_ID, USER_PW, USER_NAME, RDATE, MDATE FROM USERS WHERE USER_ID = ?', (user_id,), True)
        except Exception as e:
            err_log(self.logger, e, 'get_user_by_id', traceback.format_exc())
            user_info = None
        return user_info

    def insert_user(self, user_id, user_pw, user_name):
        """
        User 정보 등록
        :param user_id:
        :param user_pw:
        :param user_name:
        :return:
        """
        try:
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
            Sqlite3().cmd('INSERT INTO USERS (USER_ID, USER_PW, USER_NAME, RDATE, MDATE) VALUES (?, ?, ?, ?, ?)',
                          (user_id, user_pw, user_name, now, now))
        except Exception as e:
            err_log(self.logger, e, 'insert_user', traceback.format_exc())

    def update_mdate(self, user_id):
        """
        수정일 변경
        :return:
        """
        try:
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
            Sqlite3().cmd('UPDATE USERS SET MDATE = ? WHERE USER_ID = ?', (now, user_id))
        except Exception as e:
            err_log(self.logger, e, 'update_mdate', traceback.format_exc())

    def update_login_mdate(self, user_id, user_pw, user_name):
        """
        로그인 처리 및 최종 로그인일 변경
        :param user_id:
        :param user_pw:
        :param user_name:
        :return:
        """
        if self.get_user_by_id(user_id):
            self.update_mdate(user_id)
        else:
            self.insert_user(user_id, user_pw, user_name)
