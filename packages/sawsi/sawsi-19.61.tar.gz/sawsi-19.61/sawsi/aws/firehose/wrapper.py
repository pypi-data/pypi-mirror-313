import tempfile
from sawsi.aws import shared


class Firehose:
    def __init__(self, boto3_session, region=shared.DEFAULT_REGION):
        self.client = boto3_session.client('firehose', region_name=region)
        self.region = region


    def create_delivery_stream(self, delivery_stream_name, role_arn, s3_bucket_name, object_key_prefix, error_prefix='error_logs'):
        """
        Kinesis Firehose Delivery Stream 생성
        :param delivery_stream_name: 스트림 이름
        :param role_arn: S3에 쓸때 필요한 권한
        :param s3_bucket_name: 저장할 S3 이름
        :param object_key_prefix: 저장시 객체 이름 프리픽스 (EX: "item")
        :param error_prefix: 에러 발생시 객체 이름 프리픽스
        :return:
        """
        firehose_response = self.client.create_delivery_stream(
            DeliveryStreamName=delivery_stream_name,
            S3DestinationConfiguration={
                'RoleARN': role_arn,
                'BucketARN': 'arn:aws:s3:::{}'.format(s3_bucket_name),
                'Prefix': f'{object_key_prefix}/',  # 필요에 따라 수정
                'ErrorOutputPrefix': f'{error_prefix}/'  # 필요에 따라 수정
            }
        )
        return firehose_response


    def put_record(self, delivery_stream_name, data):
        """
        :param delivery_stream_name:
        :param data: Data can be binary, dict, str, ...any
        :return:
        """
        response = self.client.put_record(
            DeliveryStreamName=delivery_stream_name,
            Record={
                'Data': data
            }
        )
        return response