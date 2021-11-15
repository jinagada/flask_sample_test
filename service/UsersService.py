import logging
import sqlite3 as sql
from datetime import datetime

from service.LogService import err_log
from service.Sqlite3Serivce import dict_factory


class UsersService:
    """
    Users 데이터 처리
    """

    def __init__(self):
        """
        Class 생성 및 변수선언
        """
        self.db_logger = logging.getLogger('flask_sample_test.UsersService')
        self.db_conn = None

    def _get_db(self):
        """
        Database Connection Open
        :return:
        """
        if self.db_conn is None:
            self.db_conn = sql.connect('users.db')
            self.db_conn.row_factory = dict_factory

    def _close_db(self):
        """
        Database Connection Close
        :return:
        """
        if self.db_conn:
            self.db_conn.close()
            self.db_conn = None

    def get_user_by_id(self, user_id):
        """
        User 정보 조회
        :param user_id:
        :return:
        """
        try:
            self._get_db()
            cur = self.db_conn.cursor()
            cur.execute('SELECT USER_ID, USER_PW, USER_NAME, RDATE, MDATE FROM USERS WHERE USER_ID = ?', (user_id,))
            user_info = cur.fetchone()
            cur.close()
        except Exception as e:
            err_log(self.db_logger, e, 'get_user_by_id')
            user_info = None
        finally:
            self._close_db()
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
            self._get_db()
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
            self.db_conn.execute('INSERT INTO USERS (USER_ID, USER_PW, USER_NAME, RDATE, MDATE) VALUES (?, ?, ?, ?, ?)',
                                 (user_id, user_pw, user_name, now, now))
            self.db_conn.commit()
        except Exception as e:
            err_log(self.db_logger, e, 'insert_user')
        finally:
            self._close_db()

    def update_mdate(self, user_id):
        """
        수정일 변경
        :return:
        """
        try:
            self._get_db()
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
            self.db_conn.execute('UPDATE USERS SET MDATE = ? WHERE USER_ID = ?', (now, user_id))
            self.db_conn.commit()
        except Exception as e:
            err_log(self.db_logger, e, 'update_mdate')
        finally:
            self._close_db()

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
