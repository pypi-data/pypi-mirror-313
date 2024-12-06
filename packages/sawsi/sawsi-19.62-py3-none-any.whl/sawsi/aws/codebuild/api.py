import boto3
from sawsi.aws import shared
from typing import List, Literal, Optional


class CodeBuildAPI:
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
        self.client = boto3.client('codebuild', region_name=region)

    def batch_get_builds(self, build_ids: List[str]):
        # 커밋 기반으로 파일 가쟈오기
        response = self.client.batch_get_builds(
            ids=build_ids  # 여기에 조회하고자 하는 빌드 ID를 리스트 형태로 입력
        )
        return response

    def list_builds_for_project(self, project_name: str, sort_order: Literal["DESCENDING", "ASCENDING"] = 'DESCENDING', next_token: Optional[str] = None):
        # 빌드 정보 목록 조회
        payload = {
            'projectName': project_name,
            'sortOrder': sort_order,
        }
        if next_token:
            payload['nextToken'] = next_token
        response = self.client.list_builds_for_project(**payload)
        return response


if __name__ == '__main__':
    pass