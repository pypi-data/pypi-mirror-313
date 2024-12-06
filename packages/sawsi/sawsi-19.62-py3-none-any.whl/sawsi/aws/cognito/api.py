import time
import boto3
from sawsi.aws import shared
import hmac
import hashlib
import base64


def get_secret_hash(username, client_id, client_secret):
    msg = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'),
                   msg=str(msg).encode('utf-8'),
                   digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()


class CognitoAPI:
    """
    S3 를 활용하는 커스텀 ORM 클래스
    """
    def __init__(self, user_poop_id, client_id, client_secret, credentials=None, region=shared.DEFAULT_REGION):
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
        self.client = boto3.client('cognito-idp', region_name=region)
        self.user_pool_id = user_poop_id
        self.client_id = client_id
        self.region = region
        self.client_secret = client_secret

    def sign_up(self, phone_number, username, password):
        """
        인증번호를 사용자한테 전송합니다.
        :param username:
        :param password:
        :param phone_number:
        :return:
        """
        try:
            response = self.client.sign_up(
                ClientId=self.client_id,
                SecretHash=get_secret_hash(username, self.client_id, self.client_secret),
                Username=username,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'phone_number',
                        'Value': phone_number
                    }
                ]
            )
            return response
        except self.client.exceptions.UsernameExistsException as ex:  #  이미 회원이 존재하는 경우
            # 비활성화 상태인 경우에만 다시 전송을 허용하고, 할성 상태면 그대로 에러를 래이즈
            if self.check_user_valid(phone_number):
                raise ex
            else:
                response = self.resend_confirmation_code(username)
                return response

    def check_user_valid(self, phone_number_to_search):
        response = self.client.list_users(
            UserPoolId=self.user_pool_id,
            Filter=f'phone_number = "{phone_number_to_search}"',
            Limit=60
        )
        filtered_users = response['Users']
        # 확인된 사용자만 반환
        filtered_users = [filtered_user for filtered_user in filtered_users
                          if filtered_user['UserStatus'] == 'CONFIRMED']
        print('filtered_users:', filtered_users)
        if filtered_users:
            return True
        else:
            return False

    def resend_confirmation_code(self, username):
        response = self.client.resend_confirmation_code(
            ClientId=self.client_id,
            SecretHash=get_secret_hash(username, self.client_id, self.client_secret),
            Username=username
        )
        return response

    def confirm_sign_up(self, username, code):
        response = self.client.confirm_sign_up(
            ClientId=self.client_id,
            SecretHash=get_secret_hash(username, self.client_id, self.client_secret),
            Username=username,
            ConfirmationCode=code
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Signup confirmed!")
        else:
            print("Error in confirming signup!")
        return response

    def is_user_exists_by_phone(self, phone_number):
        try:
            # Search for the user based on the phone number
            response = self.client.list_users(
                UserPoolId=self.user_pool_id,
                Filter=f'phone_number="{phone_number}"',
            )
            # Check if any user is found with the given phone number
            return 'Users' in response and len(response['Users']) > 0
        except Exception as e:
            print(f"Error checking user by phone number: {e}")
            return False

    def cognito_login(self, user_name, phone_number, password):
        try:
            response = self.client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': phone_number,
                    'PASSWORD': password,
                    'SECRET_HASH': get_secret_hash(user_name, self.client_id, self.client_secret)
                },
                ClientId=self.client_id,

            )
            status = response.get('ChallengeName')
            session = response['Session']
            return {
                'status': status,
                'session': session,
            }

        except self.client.exceptions.NotAuthorizedException as ex:
            print(ex)
            return {
                'status': 'invalid_credential',
                'session': None
            }
        except Exception as e:
            raise e

    def confirm_cognito_login(self, session, username, phone_number, sms_code):
        try:
            mfa_response = self.client.respond_to_auth_challenge(
                ClientId=self.client_id,
                ChallengeName='SMS_MFA',
                Session=session,
                ChallengeResponses={
                    'USERNAME': phone_number,
                    'SMS_MFA_CODE': sms_code,
                    'SECRET_HASH': get_secret_hash(username, self.client_id, self.client_secret)
                },
            )
        except self.client.exceptions.NotAuthorizedException as ex:
            print(ex)
            return {
                'status': 'invalid_credential'
            }
        except Exception as e:
            raise e

        if mfa_response.get('AuthenticationResult'):
            # 성공적으로 인증된 경우
            tokens = mfa_response['AuthenticationResult']
            return {
                'status': 'success',
                'access_token': tokens['AccessToken'],
                'refresh_token': tokens.get('RefreshToken'),
                'id_token': tokens['IdToken'],
                'token_type': tokens['TokenType'],
                'expires_in': tokens['ExpiresIn']
            }
        else:
            raise Exception('UNKNOWN ISSUE')

    def verify_token(self, access_token, use_cache=True):
        # Cognito Identity Provider 클라이언트 생성
        c_key = f'{access_token}{int(time.time()) // 100}'
        if use_cache:
            response = self.cache.get(c_key, None)
            if response:
                # 있으면 응답하는데, 없으면 빠이
                return response
        try:
            # GetUser API 호출하여 토큰 검증
            response = self.client.get_user(
                AccessToken=access_token
            )
            self.cache[c_key] = response
            # 검증 성공 시 사용자 정보 반환
            return response
        except self.client.exceptions.NotAuthorizedException as e:
            raise e
        except Exception as e:
            # 기타 예외 처리
            raise e


if __name__ == '__main__':
    pass