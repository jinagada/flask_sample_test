def err_log(logger, e, fn_name):
    """
    오류로그 출력
    :param logger:
    :param e:
    :param fn_name:
    """
    logger.error(f'{fn_name} Exception : {e}')
    logger.error(f'{fn_name} Exception args : {e.args}')
