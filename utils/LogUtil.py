from flask import request


def err_log(logger, e, fn_name, traceback_str=None, msg=None):
    """
    오류로그 출력
    :param logger:
    :param e:
    :param fn_name:
    :param traceback_str:
    :param msg:
    """
    logger.error(f'{fn_name} ERROR ========= START')
    if request:
        logger.error(f'{fn_name} Call URL : {request.url if request.url else ""}')
        logger.error(f'{fn_name} Call METHOD : {request.method if request.url else ""}')
        logger.error(f'{fn_name} Call FORM : {request.form.to_dict() if len(request.form) > 0 else ""}')
    logger.error(f'{fn_name} Exception : {e}')
    logger.error(f'{fn_name} Exception args : {e.args}')
    if traceback_str:
        logger.error(f'{fn_name} traceback :\n{traceback_str}')
    if msg:
        logger.error(f'{fn_name} Exception msg : {msg}')
    logger.error(f'{fn_name} ERROR ========= END')
