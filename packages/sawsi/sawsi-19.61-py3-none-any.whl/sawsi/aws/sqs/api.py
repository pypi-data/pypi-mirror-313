from sawsi.aws import shared
from sawsi.aws.sqs import wrapper


class SQSAPI:
    """
    큐 API
    """
    def __init__(self, queue_url, credentials=None, region=shared.DEFAULT_REGION):
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
        self.sqs = wrapper.SQS(self.boto3_session, region)
        self.queue_url = queue_url

    def send_message(self, message_body):
        response = self.sqs.send_message(self.queue_url, message_body)
        return response


if __name__ == '__main__':
    pass
