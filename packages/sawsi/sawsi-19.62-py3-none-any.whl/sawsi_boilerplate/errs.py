"""
앱에서 쓰일 에러를 정의합니다.
"""


from sawsi.shared.error_util import AppError


err_n = 1

def auto(err_type:str):
    global err_n
    # 자동으로 에러 카운트를 증가시킴
    err_type = err_type.capitalize()
    err_s = f'{err_type}{str(err_n).rjust(4, "0")}'
    err_n += 1
    return err_s


source_ip_not_in_allow_ips = AppError(auto('S'), 'source_ip_not_in_allow_ips')
source_ip_not_match = AppError(auto('S'), 'source_ip_not_match')
permission_denied = AppError(auto('S'), 'permission_denied')
no_session = AppError(auto('S'), 'no_session')


def print_all_errors():
    items = list(globals().items())
    for name, obj in items:
        # AppError의 인스턴스인지 확인
        if isinstance(obj, AppError):
            print(f'Code: {obj.code}, Message: {obj.message}')


if __name__ == '__main__':
    # 현재 모듈의 모든 속성을 가져옴
    print_all_errors()

