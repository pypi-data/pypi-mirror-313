import time

from sawsi.shared import error_util
from sawsi.shared import handler_util
from sawsi.handler.router import router
import errs


# 아래 핸들러는 share.error_util.AppError 에러가 발생할시에, 자동으로
# 에러를 response 객체에 담아 코드와 메시지로 구분하여 전송합니다.
@handler_util.aws_handler_wrapper(
    error_receiver=lambda errmsg: print(errmsg),  # 이 Lambda 함수를 슬랙 Webhook 등으로 대체하면 에러 발생시 모니터링이 가능합니다.
    content_type='application/json',  # 기본적으로 JSON 타입을 반환합니다.
    use_traceback=True,  # 에러 발생시 상세 값을 응답에 전달할지 유무입니다.
    ignore_app_errors=[
        errs.no_session
    ]
)
def handler(event, context):
    """
    AWS LAMBDA에서 API Gateway 를 통해 콜한 경우
    """
    # API Gateway 로부터 Lambda 에 요청이 들어오면 다음과 같이 body 와 headers 를 분리하여 dict 형태로 반환합니다.
    body = handler_util.get_body(event, context)
    headers = handler_util.get_headers(event, context)
    source_ip = handler_util.get_source_ip(event, context)

    # 헤더로부터 세션 가져오기
    session_id = headers.get('session_id', None)

    # 아래부터는 사용자가 직접 응용하여 핸들러를 구성, 다른 함수들로 라우팅합니다.
    cmd = body.get('cmd', None)

    # user 값은 무조건 예약해서 사용해야, body 에 임의로 값을 넣어서 조작할 수 없음.
    body['user'] = None
    if session_id:
        # 주석 내용은 프로그램 내용에 따라 변경할것
        # body['user'] = some_function_to_get_user(session_id)
        pass

    # 자동 라우팅을 통해 controller 실행, 보안을 위해 사전 정의된 prefixes만 허용함.
    return router(cmd, body, headers, allowed_cmd_prefixes=[
        '{{app}}.controller'
    ])
