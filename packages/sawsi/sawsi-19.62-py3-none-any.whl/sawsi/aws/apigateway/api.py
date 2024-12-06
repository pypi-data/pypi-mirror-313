import boto3
from sawsi.aws import shared


class APIGatewayManagement:
    """
    API Gateway Management API
    """
    def __init__(self, endpoint_url, credentials=None, region=shared.DEFAULT_REGION):
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
        self.client = self.boto3_session.client('apigatewaymanagementapi', region_name=region, endpoint_url=endpoint_url)


    def post_to_connection(self, data, connection_id):
        # 커넥션에 데이터 전송
        return self.client.post_to_connection(
            Data=data,  # JSON DATA
            ConnectionId=connection_id
        )


if __name__ == '__main__':
    pass