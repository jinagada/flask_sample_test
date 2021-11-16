import logging

from utils.LogUtil import err_log


class Sqlite3Service:
    """
    Sqlite3 Database 설정
    """

    def __init__(self, db_conn):
        """
        Class 생성 시 connection 연결
        """
        self.db_logger = logging.getLogger('flask_sample_test.Sqlite3Service')
        # Connection
        self.db_conn = db_conn
        # 테이블 확인 및 생성
        if self._check_table_users() < 0:
            self._make_table_users()
        if self._check_table_boards() < 0:
            self._make_table_boards()

    def _check_table_users(self):
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
            err_log(self.db_logger, e, '_check_table_users')
        return result

    def _make_table_users(self):
        """
        테이블 생성
        :return:
        """
        try:
            self.db_conn.execute('CREATE TABLE USERS (USER_ID TEXT, USER_PW TEXT, USER_NAME TEXT, RDATE TEXT, MDATE TEXT)')
            self.db_logger.info('Maked USERS Table')
        except Exception as e:
            err_log(self.db_logger, e, '_make_table_users')

    def _check_table_boards(self):
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
            err_log(self.db_logger, e, '_check_db_boards')
        return result

    def _make_table_boards(self):
        """
        테이블 생성
        :return:
        """
        try:
            self.db_conn.execute('CREATE TABLE BOARDS (IDX INTEGER, TITLE TEXT, CONTENTS TEXT, RDATE TEXT, RUSER TEXT, MDATE TEXT, MUSER TEXT)')
            self.db_logger.info('Maked BOARDS Table')
        except Exception as e:
            err_log(self.db_logger, e, '_make_table_boards')
