import os
import threading

class LazyLoadedAPI:
    """
    LazyLoadedAPI 클래스로 다른 클래스 선언부를 감싸서, 객체의 attr 에 접근할때 초기화할 수 있도록 합니다.
    """
    def __init__(self, api_class, *args, **kwargs):
        self.api_class = api_class
        self.args = args
        self.kwargs = kwargs
        self._instance = None
        self._lock = threading.Lock()

    def _initialize_instance(self):
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = self.api_class(*self.args, **self.kwargs)

    def __getattr__(self, name):
        self._initialize_instance()
        return getattr(self._instance, name)
