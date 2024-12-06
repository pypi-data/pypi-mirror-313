import boto3
from sawsi.aws import shared
from typing import List


class LogsAPI:
    def __init__(self, credentials=None, region=shared.DEFAULT_REGION):
        """
        :param credentials: {
            "aws_access_key_id": "str",
            "aws_secret_access_key": "str",
            "region_name": "str",
            "profile_name": "str",
        }
        """
        self.boto3_session = shared.get_boto_session(credentials)
        self.cache = {}
        self.client = boto3.client('logs', region_name=region)

    def get_log_events(self, log_group_name: str, log_stream_name: str):
        # 커밋 기반으로 파일 가쟈오기
        log_events = self.client.get_log_events(
            logGroupName=log_group_name,  # 로그 그룹 이름
            logStreamName=log_stream_name  # 로그 스트림 이름
        )
        return log_events


if __name__ == '__main__':
    pass