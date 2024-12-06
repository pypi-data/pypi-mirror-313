from typing import Literal

class SMS:
    def __init__(self, boto3_session, region_name='us-east-1'):
        self.client = boto3_session.client('sns', region_name=region_name)
        self.region = boto3_session.region_name

    def send_sms(self, phone, message, sms_type: Literal["Transactional", "Promotional"]):
        body = {
            'PhoneNumber': phone,  # 전화번호
            'Message': message,  # 메시지 내용
        }
        if sms_type:
            body['MessageAttributes'] = {  # 메시지 속성 설정 (옵션)
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': sms_type  # 'Promotional' 또는 'Transactional'
                }
            }
        response = self.client.response = self.client.publish(
            **body
        )
        return response
