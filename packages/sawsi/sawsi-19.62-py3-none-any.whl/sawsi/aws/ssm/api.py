from sawsi.aws import shared
from sawsi.aws.ssm import wrapper


class SSMAPI:
    """
    시스템 매니저 API
    """
    def __init__(self, instance_id:str, credentials=None, region=shared.DEFAULT_REGION):
        """
        :param credentials: {
            "aws_access_key_id": "str",
            "aws_secret_access_key": "str",
            "region_name": "str",
            "profile_name": "str",
        }
        """
        self.boto3_session = shared.get_boto_session(credentials)
        self.region_name = region
        self.instance_id = instance_id
        self.ssm = wrapper.SSM(self.boto3_session, region)

    def run_commands(self, commands):
        """
        :param instance_id: 인스턴스 ID
        :param commands: 명령어 리스트
        :return:
        """
        return self.ssm.run_commands(self.instance_id, commands)


if __name__ == '__main__':
    pass
