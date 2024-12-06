import boto3


class SNS:
    def __init__(self, boto3_session, region_name='us-east-1'):
        self.client = boto3_session.client('sns', region_name=region_name)
        self.region = boto3_session.region_name

    def send_message_to_topic(self, topic_arn, message):
        """

        :param topic_arn: AWS에서 생성한 SNS 토픽 ARN
        :param message: message to send
        :return:
        """
        # 메시지 발행
        response = self.client.publish(
            TopicArn=topic_arn,
            Message=message,
        )
        return response
