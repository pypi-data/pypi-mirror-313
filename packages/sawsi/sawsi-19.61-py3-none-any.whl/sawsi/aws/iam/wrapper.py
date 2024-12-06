import json
from sawsi.aws import shared


class IAM:
    def __init__(self, boto3_session, region=shared.DEFAULT_REGION):
        self.client = boto3_session.client('iam')
        self.region = region


    def create_role(self, role_name, trust_policy, description='SAWSI Generated Role'):
        """
        IAM 역할 생성
        :param role_name:
        :param trust_policy:
        :param description
        :return:
        """
        role_response = self.client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description=description
        )
        return role_response


    def put_role_policy(self, role_name, policy_name, policy):
        """
        # 인라인 정책을 IAM 역할에 연결
        :param role_name:
        :param policy_name:
        :param policy:
        :return:
        """
        response = self.client.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy)
        )
        return response

    def get_role(self, role_name):
        response = self.client.get_role(RoleName=role_name)
        return response
