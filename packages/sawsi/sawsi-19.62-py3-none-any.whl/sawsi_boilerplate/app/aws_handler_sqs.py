from sawsi.shared import error_util
from sawsi.shared import handler_util
from sawsi.shared.function_util import try_run
from concurrent.futures import ThreadPoolExecutor
import json


# 아래 핸들러는 share.error_util.AppError 에러가 발생할시에, 자동으로
# 에러를 response 객체에 담아 코드와 메시지로 구분하여 전송합니다.
@handler_util.aws_handler_wrapper(
    error_receiver=lambda errmsg: print(errmsg),  # 이 Lambda 함수를 슬랙 Webhook 등으로 대체하면 에러 발생시 모니터링이 가능합니다.
    content_type='application/json',  # 기본적으로 JSON 타입을 반환합니다.
    use_traceback=True,  # 에러 발생시 상세 값을 응답에 전달할지 유무입니다.
)
def handler(event, context):
    """
    AWS LAMBDA에서 SQS 를 통해 트리거된 경우
    """
    records = event.get('Records', [])
    futures = []
    with ThreadPoolExecutor(max_workers=4) as worker:
        for record in records:
            futures.append(worker.submit(try_run, route_record, record))

    # futures 까보면서 에러 있는거 있으면 전송
    for future in futures:
        result, exception, traceback = future.result()
        # 아래 주석을 해제하면 실행 중 에러가 날시에 SQS에서 재시도를 합니다. 신중하게 처리해주세요.
        # if exception:
        #     raise Exception(f'{exception}\n{traceback}')

    return {}


def route_record(record):
    message_body = record.get('body', '{}')
    message_body = json.loads(message_body)
    body = message_body.get('body', {})
    body_type = message_body.get('type', None)
    # SQS 레코드를 읽어서 작업을 수행 합니다.
    # SQS 는 api.py 파일의 sqs 인스턴스의 def send_message(self, message_body) 함수를 콜 하여 콜 할 수 있습니다.
    # 재귀 호출로 인해 비용이 비정상적으로 발생할 수 있음을 유의하세요.

    if body_type == '{{SQS를 콜한 측에서 설정한 body_type}}':
        # TODO YOU SHOULD IMP HERE
        # TASK(body)
        return

    raise error_util.NO_SUCH_BODY_TYPE_BY_SQS