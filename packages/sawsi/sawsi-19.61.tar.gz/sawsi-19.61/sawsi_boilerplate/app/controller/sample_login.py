"""
This is sample code to tell how to use sawsi framework.
You could delete this file after know how to use this framework.
"""
from {{app}}.model.sample_user import User
from pydantic import validate_call
from sawsi.handler.controller_decorator import controller

@controller
@validate_call
def login(email:str, password:str):
    return {
        'status': 'succeed'
    }


@controller
@validate_call  # session_id 에 int 등이 등어가면 에러가 레이즈됩니다.
def get_me(session_id:str):
    # Get Data Model from DAO
    user_id = some_function_session_id_to_user_id(session_id)
    user = User.get(user_id)
    user_view_model = user.view()
    return {
        'user': user_view_model
    }


@controller
def some_function_session_id_to_user_id(session_id: str)->str:
    # DEMO FUNCTION
    return 'USER_ID'