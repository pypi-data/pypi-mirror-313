import json
import io
import time

from sawsi.aws import shared
from sawsi.aws.s3 import wrapper as s3_wrapper
from sawsi.aws.iam import wrapper as iam_wrapper
from sawsi.aws.firehose import wrapper as firehose_wrapper
from json import JSONDecodeError


def _aws_jsons_to_json(content):
    # AWS 의 json 델리미터 (구분자) 가 없어서, 아래같은 특수한 방식으로 가져와야 함.
    decoder = json.JSONDecoder()

    content_length = len(content)
    decode_index = 0
    objs = []
    while decode_index < content_length:
        try:
            obj, decode_index = decoder.raw_decode(content, decode_index)
            objs.append(obj)
        except JSONDecodeError as e:
            print("JSONDecodeError:", e)
            # Scan forward and keep trying to decode
            decode_index += 1
    return objs


class Firehose:
    """
    Firehose API
    """
    def __init__(self, delivery_stream_name, bucket_name, object_key_prefix, error_prefix='error', credentials=None, region=shared.DEFAULT_REGION):
        """
        :param delivery_stream_name:
        :param bucket_name: S3는 재활용할수도 있습니다.
        :param object_key_prefix:
        :param error_prefix:
        :param credentials: {
            "aws_access_key_id": "str",
            "aws_secret_access_key": "str",
            "region_name": "str",
            "profile_name": "str",
        }
        """
        self.boto3_session = shared.get_boto_session(credentials)
        self.cache = {}
        self.delivery_stream_name = delivery_stream_name
        self.bucket_name = bucket_name
        self.object_key_prefix = object_key_prefix
        self.error_prefix = error_prefix
        self.s3 = s3_wrapper.S3(self.boto3_session, region=region)
        self.iam = iam_wrapper.IAM(self.boto3_session, region=region)
        self.firehose = firehose_wrapper.Firehose(self.boto3_session, region=region)

    def init(self):
        """
        실제 버킷 생성 및 Firehose 생성, IAM 연결
        :param: object_key_prefix: "ITEM"
        :param: error_prefix: "ERROR"
        :return:
        """
        self.s3.init_bucket(self.bucket_name)

        role_name = f'RoleKinesis-{self.delivery_stream_name}-{self.bucket_name}'
        role_arn = self._create_role_to_access_s3(role_name)
        self._put_role_policy_to_access_s3(role_name)
        retry_count = 0
        while True:
            try:
                time.sleep(4)
                # 캐시 생성시간 때문에 에러가 날수도 있어서
                self.firehose.create_delivery_stream(
                    self.delivery_stream_name, role_arn, self.bucket_name, self.object_key_prefix, self.error_prefix
                )
                break
            except Exception as ex:
                retry_count += 1
                if retry_count > 2:
                    break
                print(ex)

    def _create_role_to_access_s3(self, role_name):
        # Firehose 에서 S3 접속을 위한 롤 생성
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "firehose.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        try:
            # IAM 역할 생성
            role_response = self.iam.create_role(
                role_name=role_name, trust_policy=trust_policy, description='Role for Kinesis Firehose to access S3'
            )
            role_arn = role_response['Role']['Arn']
            return role_arn
        except self.iam.client.exceptions.EntityAlreadyExistsException:
            # 역할이 이미 있는 경우 해당 Role의 ARN을 가져온다
            role = self.iam.get_role(role_name)
            return role['Role']['Arn']
        except Exception as ex:
            print('에러 발생:', ex)
            raise ex


    def _put_role_policy_to_access_s3(self, role_name):
        # S3 버킷에 대한 인라인 정책 정의
        s3_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:AbortMultipartUpload",
                        "s3:GetBucketLocation",
                        "s3:GetObject",
                        "s3:ListBucket",
                        "s3:ListBucketMultipartUploads",
                        "s3:PutObject"
                    ],
                    "Resource": [
                        "arn:aws:s3:::{}".format(self.bucket_name),
                        "arn:aws:s3:::{}/*".format(self.bucket_name)
                    ]
                }
            ]
        }
        try:
            # 인라인 정책을 IAM 역할에 연결
            self.iam.put_role_policy(role_name, 'S3AccessPolicy', s3_policy)
        except Exception as ex:
            print(ex)


    def put_record(self, data):
        """
        파이어호스에 Data 를 삽입합니다.
        :param data: str or bytes
        :return:
        """
        response = self.firehose.put_record(
            self.delivery_stream_name, data
        )
        return response

    def list_objects_v2(self, continuation_token, start_after=None, limit=1000):
        """
        버킷에 있는 객체들을 순환
        :param continuation_token:
        :param start_after:
        :param limit:
        :return:
        """
        response = self.s3.list_objects_v2(bucket_name=self.bucket_name,
                                           prefix=self.object_key_prefix,
                                           limit=limit,
                                           start_after=start_after,
                                           continuation_token=continuation_token)
        return response

    def generate_object_keys(self, start_after=None, limit=1000):
        """
        버킷에 있는 객체들을 순차대로 가져옵니다.
        :param prefix:
        :param start_after:
        :param limit:
        :return:
        """
        continuation_token = None
        response = self.list_objects_v2(continuation_token, start_after, limit)
        continuation_token = response.get('NextContinuationToken', None)
        contents = response.get('Contents', [])
        for content in contents:
            yield content
        while continuation_token:
            response = self.list_objects_v2(continuation_token, start_after, limit)
            continuation_token = response.get('NextContinuationToken', None)
            contents = response.get('Contents', [])
            for content in contents:
                yield content

    def generate_log_json_list_and_key(self, key_start_after=None):
        """
        prefix 로 시작하는, start_after key 지점부터 모든
        log 들을 읽고 내부 컨텐츠를 json 으로 변환하여 list 만들어 출력
        :param key_start_after:
        :return:
        """
        for content in self.generate_object_keys(key_start_after):
            last_key = content['Key']
            buffer = io.BytesIO()
            self.s3.client.download_fileobj(self.bucket_name, last_key, buffer)
            buffer.seek(0)
            item_bytes = buffer.read()
            item_string = item_bytes.decode('utf-8')
            objects = _aws_jsons_to_json(item_string)
            yield objects, last_key


if __name__ == '__main__':
    pass
