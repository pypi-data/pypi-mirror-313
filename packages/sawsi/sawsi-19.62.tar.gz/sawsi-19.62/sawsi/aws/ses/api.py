from sawsi.aws import shared
from sawsi.aws.ses import wrapper


class SESAPI:
    """
    키 등을 관리하는 API
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
        self.sns = wrapper.SES(self.boto3_session, region)

    def send_email(self, sender, recipient, subject, body_text, body_html):
        response = self.sns.send_email(sender, recipient, subject, body_text, body_html)
        return response


if __name__ == '__main__':
    pass