"""
핸들러에서 쓰이는 유틸
에러수집 or payload, user 로 바꾸는 부분
에러 수정 유틸.
"""
import traceback
import json
from sawsi.shared import error_util
from sawsi.shared import dict_util
from typing import List
import time


def get_body(event, context):
    """
    API로부터 요청된 body 를 반환합니다.
    :param event:
    :param context:
    :return: dict
    """
    body = event.get('body', None)
    if body:
        try:
            return json.loads(body)
        except Exception as ex:
            print(ex)
    return body


def get_headers(event, context):
    """
    API로부터 요청된 headers 를 반환합니다.
    :param event:
    :param context:
    :return: dict
    """
    headers = event.get('headers', {})
    return headers


def get_source_ip(event, context):
    """
    요청지의 소스IP를 얻어냅니다.
    :param event:
    :param context:
    :return: 52.411.555.11 (EX)
    """
    request_context = event.get('requestContext', {})
    client_ip = request_context.get('identity', {}).get('sourceIp', '0.0.0.0')
    return client_ip


def aws_handler_wrapper(error_receiver=None, content_type='application/json', use_traceback=True, ignore_app_errors:List[error_util.AppError]=[]):  # 데코레이터 팩토리
    """
    핸들러를 감싸고, 해당 코드에서 에러가 발생하면,
    error_receiver(message) 형식으로 콜백이 이루어집니다.
    외부에서 해당 에러 메시지를 Slack 에 전송하거나 기타 알림을 수행합니다.
    :param error_receiver: def some_function_to_notice_error_message(message: str)
    :param content_type: 'application/json' 등의 반환되는 콘텐츠 타입입니다.
    :param use_traceback: 에러 발생시, 상세 내용 전파 여부입니다.
    :param ignore_app_errors: error_util.AppError 객체 중 error_receiver 에 보내지 않을 객체입니다.
    :return:
    """
    def _handler_wrapper(func):
        """
        엔트리 핸들러에는 이 데코레이터를 붙여준다.
        반환되는 응답에 코드화를 해줍니다.
        :param func:
        :return:
        """
        def decorator(*args, **kwargs):
            now = time.time()
            # print(args, kwargs)
            try:
                result = func(*args, **kwargs)
                if result is None:
                    result = {}
                if isinstance(result, dict) and 'rslt_cd' not in result:
                    # 없으면 기본으로 삽입
                    result['rslt_cd'] = 'A00000'
                    result['rslt_msg'] = '요청 성공'
                    result['duration'] = time.time() - now
                aws_response = AWSResponse(result, content_type=content_type)
                # print(aws_response)
                return aws_response
            except error_util.AppError as ex:
                result = {
                    'rslt_cd': str(ex.code),
                    'rslt_msg': str(ex.message),
                    'duration': time.time() - now
                }
                if use_traceback:
                    result['traceback'] = str(traceback.format_exc())
                if error_receiver:
                    try:
                        if ignore_app_errors and ex.code in {ignore_app_error.code for ignore_app_error in ignore_app_errors}:
                            # 무시
                            pass
                        else:
                            message = error_util.make_error_description(args[0])
                            error_receiver(message)
                    except Exception as ex:
                        result['error_receiver_failed_exc'] = str(ex)
                aws_response = AWSResponse(result)
                # print(aws_response)
                return aws_response
            except Exception as ex:
                result = {
                    # 알수없는에러
                    'rslt_cd': 'U99999',
                    'rslt_msg': str(ex),
                    'duration': time.time() - now
                }
                if use_traceback:
                    result['traceback'] = str(traceback.format_exc())
                if error_receiver:
                    try:
                        message = error_util.make_error_description(args[0])
                        error_receiver(message)
                    except Exception as ex:
                        result['error_receiver_failed_exc'] = str(ex)
                aws_response = AWSResponse(result)
                # print(aws_response)
                return aws_response
        return decorator
    return _handler_wrapper


def _get_headers(content_type='application/json', charset='UTF-8'):
    api_gateway_response_header = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': 'POST,OPTIONS,GET',
        'Content-Type': content_type,
        'charset': charset
    }
    return api_gateway_response_header


class AWSResponse(dict):
    def __init__(self, body, content_type='application/json', status_code=200, charset='UTF-8'):
        headers = _get_headers(content_type, charset=charset)
        self['statusCode'] = status_code
        self['headers'] = headers
        if isinstance(body, dict):
            body = dict_util.convert_decimal_to_number(body)  # 숫자 변경을 위해
            self['body'] = json.dumps(body, default=lambda o: '<not serializable>')
        else:
            self['body'] = body
        self['isBase64Encoded'] = False
