from sawsi.shared import handler_util
from sawsi.shared.schedule_util import ScheduledTask, join

# X-ray 추적


# 아래 핸들러는 share.error_util.AppError 에러가 발생할시에, 자동으로
# 에러를 response 객체에 담아 코드와 메시지로 구분하여 전송합니다.
@handler_util.aws_handler_wrapper(
    error_receiver=lambda errmsg: print(errmsg),  # 이 Lambda 함수를 슬랙 Webhook 등으로 대체하면 에러 발생시 모니터링이 가능합니다.
    content_type='application/json',  # 기본적으로 JSON 타입을 반환합니다.
    use_traceback=True,  # 에러 발생시 상세 값을 응답에 전달할지 유무입니다.
)
def handler(event, context):
    """
    AWS CloudWatch Event Bridge - Scheduler 를 통해 트리거됨
    중요: 일정을 (Rate 1 minute) 으로 설정시 자동으로 아래 함수들이 맞는 일정에 맞춰 실행 됨.
    """
    # 매일 0시 0분에 수행
    with ScheduledTask('0 0 * * *') as do:
        def task_to_do():
            # SHOULD IMP
            # TASK ...
            pass

        do(task_to_do)

    # 15분 마다 수행
    with ScheduledTask('*/15 * * * *') as do:
        def task_to_do_1():
            # TASK ...
            # SHOULD IMP
            pass

        def task_to_do_2():
            # TASK ...
            # SHOULD IMP
            pass

        do(task_to_do_1)
        do(task_to_do_2)

    # Join until task is done
    join()