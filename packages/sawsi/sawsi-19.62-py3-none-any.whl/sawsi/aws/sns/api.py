from sawsi.aws import shared
from sawsi.aws.sns import wrapper


class SNSAPI:
    """
    이메일 전송 API
    """
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
        self.region_name = region
        self.sns = wrapper.SNS(self.boto3_session, region)

    def send_message(self, topic_arn, message):
        response = self.sns.send_message_to_topic(topic_arn, message)
        return response


if __name__ == '__main__':
    pass
