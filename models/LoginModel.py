class LoginModel(dict):
    """
    Login 정보
    “TypeError: Object of type LoginModel is not JSON serializable” 에러를 피하기 위해 dict 를 상속 받아서 Model Class 를 만든다.
    """
    def __init__(self, user_id, user_pw):
        dict.__init__(self, user_id=user_id, user_pw=user_pw)
