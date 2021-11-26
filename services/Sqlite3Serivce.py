import logging
import traceback

from datasources.Sqlite3 import Sqlite3
from utils.LogUtil import err_log


class Sqlite3Service:
    """
    Sqlite3 Database 설정
    """

    def __init__(self):
        """
        Class 생성
        """
        self.logger = logging.getLogger('flask_sample_test.services.Sqlite3Service')
        # 테이블 확인 및 생성
        if self._check_table_users() < 0:
            self._make_table_users()
            # 최초 사용자 등록
            self._insert_first_user()
        if self._check_table_boards() < 0:
            self._make_table_boards()
        if self._check_table_files() < 0:
            self._make_table_files()

    def _check_table_users(self):
        """
        테이블 확인
        :return:
        """
        try:
            tmp = Sqlite3().execute(query='SELECT COUNT(*) AS CNT FROM USERS')
            result = tmp[0]['CNT']
            self.logger.info(f'Check USERS Table : {result}')
        except Exception as e:
            err_log(self.logger, e, 'Sqlite3Service._check_table_users', traceback.format_exc())
            result = -1
        return result

    def _insert_first_user(self):
        """
        최초 사용자 등록
        :return:
        """
        try:
            result = Sqlite3().cmd(query='INSERT INTO USERS (USER_ID, USER_PW, USER_NAME, RDATE, MDATE) VALUES (\'admin\', \'1234!\', \'Admin User\', DATETIME(\'now\', \'localtime\'), DATETIME(\'now\', \'localtime\'))')
            self.logger.info(f'Insert USER : {result}')
        except Exception as e:
            err_log(self.logger, e, 'Sqlite3Service._insert_first_user', traceback.format_exc())
            result = -1
        return result

    def _make_table_users(self):
        """
        테이블 생성
        :return:
        """
        try:
            Sqlite3().cmd(query='''CREATE TABLE USERS
            (SEQ INTEGER PRIMARY KEY AUTOINCREMENT,
             USER_ID TEXT UNIQUE,
             USER_PW TEXT,
             USER_NAME TEXT,
             RDATE TEXT,
             MDATE TEXT)''')
            self.logger.info('Maked USERS Table')
        except Exception as e:
            err_log(self.logger, e, 'Sqlite3Service._make_table_users', traceback.format_exc())

    def _check_table_boards(self):
        """
        테이블 확인
        :return:
        """
        try:
            tmp = Sqlite3().execute(query='SELECT COUNT(*) AS CNT FROM BOARDS')
            result = tmp[0]['CNT']
            self.logger.info(f'Check BOARDS Table : {result}')
        except Exception as e:
            err_log(self.logger, e, 'Sqlite3Service._check_db_boards', traceback.format_exc())
            result = -1
        return result

    def _make_table_boards(self):
        """
        테이블 생성
        :return:
        """
        try:
            Sqlite3().cmd(query='''CREATE TABLE BOARDS
            (SEQ INTEGER PRIMARY KEY AUTOINCREMENT,
             TITLE TEXT,
             CONTENTS TEXT,
             RDATE TEXT,
             RUSER TEXT,
             MDATE TEXT,
             MUSER TEXT)''')
            self.logger.info('Maked BOARDS Table')
        except Exception as e:
            err_log(self.logger, e, 'Sqlite3Service._make_table_boards', traceback.format_exc())

    def _check_table_files(self):
        """
        테이블 확인
        :return:
        """
        try:
            tmp = Sqlite3().execute(query='SELECT COUNT(*) AS CNT FROM FILES')
            result = tmp[0]['CNT']
            self.logger.info(f'Check FILES Table : {result}')
        except Exception as e:
            err_log(self.logger, e, 'Sqlite3Service._check_table_files', traceback.format_exc())
            result = -1
        return result

    def _make_table_files(self):
        """
        테이블 생성
        :return:
        """
        try:
            Sqlite3().cmd(query='''CREATE TABLE FILES
            (SEQ INTEGER PRIMARY KEY AUTOINCREMENT,
             BOARD_SEQ INTEGER,
             PATH TEXT,
             FNAME TEXT,
             RDATE TEXT,
             RUSER TEXT)''')
            self.logger.info('Maked FILES Table')
        except Exception as e:
            err_log(self.logger, e, 'Sqlite3Service._make_table_files', traceback.format_exc())
