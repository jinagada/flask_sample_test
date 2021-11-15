import logging
import sqlite3 as sql

from service.LogService import err_log


def dict_factory(cursor, row):
    """
    tuple -> dict
    :param cursor:
    :param row:
    :return:
    """
    new_row = {}
    for idx, col in enumerate(cursor.description):
        new_row[col[0]] = row[idx]
    return new_row


class Sqlite3UserService:
    """
    Sqlite3 Database 설정
    """

    def __init__(self):
        """
        Class 생성 시 connection 연결
        """
        self.db_logger = logging.getLogger('flask_sample_test.Sqlite3UserService')
        # Connection
        self.db_conn = None
        # 테이블 확인 및 생성
        self._get_db()
        if self._check_db() < 0:
            self._make_table()
        self._close_db()

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

    def _check_db(self):
        """
        테이블 확인
        :return:
        """
        try:
            cur = self.db_conn.cursor()
            cur.execute('SELECT COUNT(*) FROM USERS')
            tmp = cur.fetchone()
            result = tmp[0] if len(tmp) > 0 else 0
            cur.close()
            self.db_logger.info(f'Check USERS Table : {result}')
        except Exception as e:
            result = -1
            err_log(self.db_logger, e, '_check_db')
        return result

    def _make_table(self):
        """
        테이블 생성
        :return:
        """
        try:
            self._get_db()
            self.db_conn.execute('CREATE TABLE USERS (USER_ID TEXT, USER_PW TEXT, USER_NAME TEXT, RDATE TEXT, MDATE TEXT)')
            self.db_logger.info('Maked USERS Table')
        except Exception as e:
            err_log(self.db_logger, e, '_make_table')


class Sqlite3BoardService:
    """
    Sqlite3 Database 설정
    """

    def __init__(self):
        """
        Class 생성 시 connection 연결
        """
        self.db_logger = logging.getLogger('flask_sample_test.Sqlite3BoardService')
        # Connection
        self.db_conn = None
        # 테이블 확인 및 생성
        self._get_db()
        if self._check_db() < 0:
            self._make_table()
        self._close_db()

    def _get_db(self):
        """
        Database Connection Open
        :return:
        """
        if self.db_conn is None:
            self.db_conn = sql.connect('boards.db')
            self.db_conn.row_factory = dict_factory

    def _close_db(self):
        """
        Database Connection Close
        :return:
        """
        if self.db_conn:
            self.db_conn.close()
            self.db_conn = None

    def _check_db(self):
        """
        테이블 확인
        :return:
        """
        try:
            cur = self.db_conn.cursor()
            cur.execute('SELECT COUNT(*) FROM BOARDS')
            tmp = cur.fetchone()
            result = tmp[0] if len(tmp) > 0 else 0
            cur.close()
            self.db_logger.info(f'Check BOARDS Table : {result}')
        except Exception as e:
            result = -1
            err_log(self.db_logger, e, '_check_db')
        return result

    def _make_table(self):
        """
        테이블 생성
        :return:
        """
        try:
            self.db_conn.execute('CREATE TABLE BOARDS (IDX INTEGER, TITLE TEXT, CONTENTS TEXT, RDATE TEXT, RUSER TEXT, MDATE TEXT, MUSER TEXT)')
            self.db_logger.info('Maked BOARDS Table')
        except Exception as e:
            err_log(self.db_logger, e, '_make_table')
