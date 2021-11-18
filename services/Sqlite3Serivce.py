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
        self.logger = logging.getLogger('flask_sample_test.Sqlite3Service')
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
            tmp = Sqlite3().execute(query='SELECT COUNT(*) AS CNT FROM USERS')
            result = tmp[0]['CNT']
            self.logger.info(f'Check USERS Table : {result}')
        except Exception as e:
            err_log(self.logger, e, '_check_table_users', traceback.format_exc())
            result = -1
        return result

    def _make_table_users(self):
        """
        테이블 생성
        :return:
        """
        try:
            Sqlite3().cmd(query='CREATE TABLE USERS (USER_ID TEXT, USER_PW TEXT, USER_NAME TEXT, RDATE TEXT, MDATE TEXT)')
            self.logger.info('Maked USERS Table')
        except Exception as e:
            err_log(self.logger, e, '_make_table_users', traceback.format_exc())

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
            err_log(self.logger, e, '_check_db_boards', traceback.format_exc())
            result = -1
        return result

    def _make_table_boards(self):
        """
        테이블 생성
        :return:
        """
        try:
            Sqlite3().cmd(query='CREATE TABLE BOARDS (IDX INTEGER, TITLE TEXT, CONTENTS TEXT, RDATE TEXT, RUSER TEXT, MDATE TEXT, MUSER TEXT)')
            self.logger.info('Maked BOARDS Table')
        except Exception as e:
            err_log(self.logger, e, '_make_table_boards', traceback.format_exc())
