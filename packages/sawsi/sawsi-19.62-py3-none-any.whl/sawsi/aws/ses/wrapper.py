import boto3


class SES:
    def __init__(self, boto3_session, region_name='us-east-1'):
        self.client = boto3_session.client('ses', region_name=region_name)
        self.region = boto3_session.region_name

    def send_email(self, sender, recipient, subject, body_text, body_html):
        # SES 클라이언트 생성
        ses_client = self.client
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [recipient],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject,
                },
            },
            Source=sender,
        )
        return response
