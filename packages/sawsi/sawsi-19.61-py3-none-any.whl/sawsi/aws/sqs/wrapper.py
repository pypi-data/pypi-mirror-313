import boto3


class SQS:
    def __init__(self, boto3_session, region_name='us-east-1'):
        self.client = boto3_session.client('sqs', region_name=region_name)
        self.region = boto3_session.region_name


    def send_message(self, queue_url, message_body):
        response = self.client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        return response
