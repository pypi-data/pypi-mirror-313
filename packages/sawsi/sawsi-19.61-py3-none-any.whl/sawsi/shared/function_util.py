"""
Handler layer (상위 레이어)의 데코레이터
"""
import threading


def auto_cache(func):
    """
    이 데코레이터를 삽입하면 파라메터가 동일할시에 캐싱된 값을 사용
    :param func:
    :return:
    """
    storage = {}

    def decorator(*args, **kwargs):
        key = f'{str(args)}-{str(kwargs)}'
        if key in storage and kwargs.get('use_cache', True):
            return storage[key]
        result = func(*args, **kwargs)
        storage[key] = result
        return result
    return decorator


def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


def try_run(func, *args, **kwargs):
    """
    func 을 실행 후 에러가 있으면 에러 객체를 반환.
    스레드 에러 처리를 위해 사용합니다.
    :param func:
    :param args:
    :param kwargs:
    :return: (result, exception, traceback)
    """
    try:
        return func(*args, **kwargs), None, None
    except Exception as ex:
        import traceback
        return None, ex, traceback.format_exc()
