from sawsi.aws import shared
from typing import Any


class LambdaAPI:
    def __init__(self, credentials=None, region=shared.DEFAULT_REGION):
        self.boto3_session = shared.get_boto_session(credentials)
        self.lambda_client = self.boto3_session.client('lambda', region_name=region)

    def invoke(self, function_name: str, payload: Any):
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # 'Event' for asynchronous execution
            Payload=payload
        )

        # 응답에서 Payload 추출
        response_payload = response['Payload'].read()
        response_body = response_payload.decode('utf-8')
        return response_body

    def create_event_source_mapping(
            self, function_name: str, event_source_arn: str,
            enabled: bool = True, batch_size: int = 100, starting_position: str = 'LATEST'
    ):
        """
        Lambda 함수에 트리거 추가
        """
        response = self.lambda_client.create_event_source_mapping(
            EventSourceArn=event_source_arn,
            FunctionName=function_name,
            Enabled=enabled,
            BatchSize=batch_size,  # 처리할 항목 수 조정 가능
            StartingPosition=starting_position  # 최신 항목부터 시작
        )
        return response
