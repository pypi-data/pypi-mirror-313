"""
에러 핸들링에 필요한 유틸,
외부 채널을 통해 에러를 모니터링할수 있도록 도와줍니다.
"""
import traceback
import pprint
from datetime import datetime


class AppError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return repr(f'app_error => code: {self.code}, message: {self.message}')

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message
        }


SYSTEM_NO_SUCH_CMD = AppError('B00001', 'No such cmd')
IDX_OFFSET_MUST_BE_NUMBER = AppError('B00002', 'IDX_OFFSET_MUST_BE_NUMBER')
LIMIT_MUST_LESS_EQUAL_1000 = AppError('B00003', 'LIMIT_MUST_LESS_EQUAL_1000')
SHOULD_USE_S3OBJECT_S_IN_QUERY = AppError('B00004', 'Should make query like this => "SELECT * FROM S3Object s WHERE s.<field> = <value>"')
NO_SUCH_BODY_TYPE_BY_SQS = AppError('B00005', 'NO_SUCH_BODY_TYPE_BY_SQS')
Command_Prefix_not_allowed = AppError('B00006', 'Command_Prefix_not_allowed')


def make_error_description(event):
    # 에러 발생시 설명을
    tb = traceback.format_exc()
    source_ip = event.get('requestContext', {}).get('identity', {}).get('sourceIp', None)
    request_id = event.get('requestContext', {}).get('requestId', None)

    request_payload_str = pprint.pformat(event, indent=1)
    if len(request_payload_str) > 3000:
        request_payload_str = request_payload_str[:3000]  # 1000글자 제한
        request_payload_str += '... \n*See more to query via AWS Cloudwatch, Copy & Paste bellow!*'
        request_payload_str += '```fields @timestamp, @message\n' +\
                               f' | filter requestContext.requestId = "{request_id}"\n' +\
                                ' | sort @timestamp desc\n' +\
                                ' | limit 20```\n'

    description = f'>*{datetime.now()}*\n' \
                  f'>*source_ip*: {source_ip}\n' \
                  f'>*request_id*: {request_id}\n\n' \
                  f'>*요청(1000글자):*\n{request_payload_str}\n\n' \
                  f'>*에러*:\n{tb}\n\n'
    return description


if __name__ == '__main__':
    r = make_error_description({})
    print(r)

