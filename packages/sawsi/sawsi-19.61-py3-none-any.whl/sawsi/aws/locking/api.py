"""
DynamoDB 를 사용하기 위한 인터페이스
"""
import time
import contextlib
from sawsi.aws.locking import wrapper
from sawsi.aws import shared


class LockingAPI:
    """
    DynamoDB를 이용한 로킹 서비스
    """
    def __init__(self, table_name, credentials=None, region=shared.DEFAULT_REGION):
        """
        :param table_name: "테이블 이름"
        :param credentials: {
            "aws_access_key_id": "str",
            "aws_secret_access_key": "str",
            "region_name": "str",
            "profile_name": "str"
        }
        """
        self.boto3_session = shared.get_boto_session(credentials)
        self.cache = {}
        self.table_name = table_name
        self.dynamoFDB = wrapper.DynamoFDB(self.boto3_session, table_name, region)

    def init_table(self):
        # 테이블을 초기화합니다.
        self.dynamoFDB.init_fdb_table()

    @contextlib.contextmanager
    def lock(self, object_key, max_alive_ts=30, max_retries=3, wait_time=2):
        """
        Lock을 획득하고 해제하는 컨텍스트 매니저.
        """
        acquired = self.acquire_lock(object_key, max_alive_ts, max_retries, wait_time)
        try:
            if not acquired:
                raise RuntimeError("Failed to acquire lock")
            yield  # with 블록 내부의 코드가 실행됩니다.
        finally:
            if acquired:
                self.release_lock(object_key)

    def acquire_lock(self, object_key, max_alive_ts=30, max_retries=3, wait_time=2):
        """
        Lock 을 얻기 위해 시도 합니다.
        :param object_key: 락 대상 객체 키
        :param max_alive_ts: 락이 살아 있을 수 있는 최대 시간 (초)
        :param max_retries: 락이 걸려 있을시 재시도 횟수
        :param wait_time: 기본 재시도 텀 (초)
        :return:
        """
        for i in range(max_retries):
            try:
                # 락을 획득하려고 시도합니다.
                self.dynamoFDB.put_item({
                    '_pk': object_key,
                    '_sk': '_',
                    'ttl': int(time.time() + max_alive_ts)
                }, can_overwrite=False)
                return True
            except Exception as e:
                lock = self.dynamoFDB.get_item(object_key, '_', consistent_read=True)
                if lock:
                    # 이미 락이 걸려 있습니다.
                    ttl = lock['ttl']
                    if ttl < time.time():
                        # 락이 죽었습니다.
                        self.dynamoFDB.delete_item(object_key, '_')
                        return True
                print(f"Lock acquisition attempt {i + 1} failed. Retrying...")
                time.sleep(wait_time)
                wait_time *= 2  # 대기 시간을 두배로 늘립니다.
        # 모든 재시도가 실패했을 경우 False를 반환합니다.
        return False

    def release_lock(self, object_key):
        """
        먼저 일관성 읽기로 아이템 존재를 보장한 후에 제거하기 위해 활용
        :param object_key:
        :return:
        """
        return self.dynamoFDB.delete_item(object_key, '_')

    def is_locked(self, object_key: str) -> bool:
        """
        락이 걸려있는지 확인용도
        :param object_key:
        :return:
        """
        item = self.dynamoFDB.get_item(object_key, '_', consistent_read=True)
        return bool(item)



if __name__ == '__main__':
    lapi = LockingAPI('locking')
    OBJECT_KEY = 'K'
    if lapi.acquire_lock(OBJECT_KEY):
        print("Lock acquired!")
        # ... 다음 작업을 수행 ...
    else:
        print("Failed to acquire lock after maximum retries.")

    lapi.release_lock(OBJECT_KEY)

