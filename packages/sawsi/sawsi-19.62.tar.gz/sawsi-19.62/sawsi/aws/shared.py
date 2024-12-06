"""
boto3 세션 등 AWS 쓰려면 공용으로 써야하는 함수들
"""
import boto3

DEFAULT_REGION = 'ap-northeast-2'


def get_boto_session(credentials=None):
    """
    시스템에서 boto3 세션을 반환하는데, 나중에 이 함수를 커스텀해야할때를 대비하여 Wrapping 해둡니다.
    credentials: {
        "aws_access_key_id": "str",
        "aws_secret_access_key": "str",
        "region_name": "str",
        "profile_name": "str",
    }
    :return:
    """
    if credentials:
        # 이걸 쓰면 보안에 좋지 않음. 하드코딩 되어있는거라.
        print('[WARNING]: credentials 을 하드코드하였습니다. AWS IAM의 환경프로파일을 이용하길 바랍니다.')
        return boto3.Session(**credentials)
    else:
        return boto3.Session()


if __name__ == '__main__':
    s = get_boto_session()
    print(s)