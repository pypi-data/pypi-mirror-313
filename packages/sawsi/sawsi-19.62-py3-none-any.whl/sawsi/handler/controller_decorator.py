"""
각 함수에 데코레이터를 적용하여 특정 경로로 라우팅되도록 만들기 위해 데코레이터를 정의합니다.
"""

controller_registry = {}



def controller(func):
    # 함수가 속한 모듈의 경로와 함수 이름을 합쳐서 full_module_name을 생성
    module_name = func.__module__  # 함수가 속한 모듈 경로를 자동으로 가져옴
    func_name = func.__name__  # 함수 이름
    full_module_name = f"{module_name}.{func_name}"

    # controller_registry에 등록
    controller_registry[full_module_name] = func

    return func
