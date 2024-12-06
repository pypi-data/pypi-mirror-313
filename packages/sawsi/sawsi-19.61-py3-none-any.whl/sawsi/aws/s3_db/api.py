from sawsi.aws import shared
from sawsi.aws.s3 import wrapper
from sawsi.aws.dynamodb import wrapper as ddb_wrapper
from sawsi.shared.filter_exp_util import Exp
from typing import List
from secrets import token_urlsafe
from sawsi.shared import error_util
import json
import contextlib
import time



def encode_dict(dict_obj):
    def cast_number(v):
        if isinstance(v, dict):
            return encode_dict(v)
        if isinstance(v, list):
            return encode_dict(v)
        if isinstance(v, bool):
            return bool(v)
        # if not isinstance(v, Number):
        #     return v
        if v % 1 == 0:
            return int(v)
        else:
            return float(v)

    if isinstance(dict_obj, dict):
        return {k: cast_number(v) for k, v in dict_obj.items()}
    elif isinstance(dict_obj, list):
        return [cast_number(v) for v in dict_obj]
    else:
        return dict_obj



class S3DBAPI:
    """
    S3 를 활용하는 DB 클래스
    순차적으로 증가하고 삭제 혹은 업데이트 되지 않는 경우 유리함.
    용량이 크고 삭제되지 않는 데이터 처리에 사용하세요.
    """
    def __init__(self, bucket_name, credentials=None, region=shared.DEFAULT_REGION):
        """
        :param bucket_name:
        :param credentials: {
            "aws_access_key_id": "str",
            "aws_secret_access_key": "str",
            "region_name": "str",
            "profile_name": "str",
        }
        """
        self.boto3_session = shared.get_boto_session(credentials)
        self.cache = {}
        self.bucket_name = bucket_name
        self.table_name = f'{self.bucket_name}-s3db'
        self.s3 = wrapper.S3(self.boto3_session, region=region)
        self.dynamoDB = ddb_wrapper.DynamoDB(self.boto3_session, region, bucket_name)

    def init(self, acl='private'):
        """
        실제 버킷 및 테이블 생성
        :return:
        """
        self.s3.init_bucket(self.bucket_name, acl)
        self.dynamoDB.create_db_table(
            self.table_name, partition_key='pk', partition_key_type='S',
            sort_key='seg', sort_key_type='S'  # seg 는 분할된 경우 1-1, 1-2 이런식으로 -n 이 추가되며, 기본 생성시는 0부터 증가
        )

    def upload_binary(self, file_name, binary):
        return self.s3.upload_binary(self.bucket_name, file_name, binary)

    def delete_binary(self, file_name):
        return self.s3.delete_binary(self.bucket_name, file_name)

    def download_binary(self, file_name):
        return self.s3.download_binary(self.bucket_name, file_name)


    def generate_metadata(self, partition, pk_field, pk_value, sk_field, start, end):
        """
        메타데이터를 조회합니다.
        :return:
        """
        partition_key_value = f'{partition}/{pk_field}=={pk_value}:{sk_field}'
        start_key = -1
        while start_key == -1 or start_key:
            response = self.dynamoDB.query_items(
                self.table_name, partition_key_name='pk', partition_key_value=partition_key_value,
                sort_key_name='seg', limit=1000, start_key=start_key, sort_condition=None, sort_key_value=None,
            )
            its = response.get('Items', [])
            if start is not None:
                its = [it for it in its if it['end'] >= start]
            if end is not None:
                its = [it for it in its if it['start'] <= end]
            for it in its:
                yield encode_dict(it)
            start_key = response.get('LastEvaluatedKey', None)

    def create_items(self, partition: str, pk_field: str, pk_value: str, sk_field: str, items: List[dict], unique_field: str):
        """
        아이템 생성, 벌크로 생성.
        생성전에 락을 걸어야하고,
        넣기전에 DDB 조회해서
        id 값이 유니크한 값으로 넣어야하는 파일에 넣고,
        파일의 용량이 50mb 를 초과하면 분할합니다.
        :return:
        """
        if not items:
            return
        object_key = f'{partition}/{pk_field}'
        partition_key_value = f'{partition}/{pk_field}=={pk_value}'
        # 락 걸기
        with self.lock(object_key=object_key):
            # DDB 조회
            sk_values = [item[sk_field] for item in items]
            start = min(sk_values)
            end = max(sk_values)
            metas = self.generate_metadata(partition, pk_field, pk_value, sk_field, start, end)



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
                self.dynamoDB.put_item(
                    self.table_name, {
                        'pk': object_key,
                        'seg': '_',
                        'ttl': int(time.time() + max_alive_ts)
                    }, can_overwrite=False
                )
                return True
            except Exception as e:
                lock = self.dynamoDB.get_item(self.table_name, {
                    'pk': object_key,
                    'seg': '_'
                }, consistent_read=True, use_cache=False)
                if lock:
                    # 이미 락이 걸려 있습니다.
                    ttl = lock['ttl']
                    if ttl < time.time():
                        # 락이 죽었습니다.
                        self.dynamoDB.delete_item(self.table_name, key={
                            'pk': object_key,
                            'seg': '_'
                        })
                        return True
                print(f"Lock acquisition attempt {i + 1} failed. Retrying...")
                time.sleep(wait_time)
                wait_time *= 2  # 대기 시간을 두배로 늘립니다.
        # 모든 재시도가 실패했을 경우 False를 반환합니다.
        return False

    def release_lock(self, object_key):
        # 먼저 일관성 읽기로 아이템 존재를 보장한 후에 제거
        return self.dynamoDB.delete_item(
            self.table_name,
            key={
                'pk': object_key,
                'seg': '_'
            }
        )

