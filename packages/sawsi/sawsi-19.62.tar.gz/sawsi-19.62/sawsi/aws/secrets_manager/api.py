import json

from sawsi.aws import shared
from sawsi.aws.secrets_manager import wrapper


class SecretManagerAPI:
    """
    키 등을 관리하는 API
    """
    def __init__(self, secret_name, credentials=None, region=shared.DEFAULT_REGION):
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
        self.secret_name = secret_name
        self.secret_manager = wrapper.SecretManager(self.boto3_session, region=region)
        # 메모리에 적재, json 으로 변경합니다. 여기서 복호화 이뤄짐.

    def _get_secret_value_response(self):
        response = self.secret_manager.get_secret_value_response(self.secret_name)
        return response

    def get_secret_value(self, key):
        """
        실제 저장된 키 값을 불러옵니다.
        :param key:
        :return:
        """
        if 'secret_value_response_json' in self.cache:
            secret_value_response_json = self.cache['secret_value_response_json']
        else:
            secret_value_response_json = json.loads(self._get_secret_value_response())
            self.cache['secret_value_response_json'] = secret_value_response_json
        return secret_value_response_json[key]
