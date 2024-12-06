from sawsi.aws.secrets_manager.api import SecretManagerAPI
from sawsi.aws.dynamodb.api import DynamoDBAPI
from sawsi.aws.s3.api import S3API
from sawsi.aws.locking.api import LockingAPI
from sawsi.aws.firehose.api import Firehose
from sawsi.aws.ses.api import SESAPI
from sawsi.aws.sqs.api import SQSAPI
import config


env = config.env
region = config.region


if not env:
    raise Exception('os.getenv() is None')


"""
Bellow codes are sample
You can modify or delete
"""

project_name = '{{project}}'

secret_manager: SecretManagerAPI = SecretManagerAPI(f'{env}/{project_name}', region=region)
dynamo = DynamoDBAPI(f'{env}-{project_name}', region=region)
s3_public = S3API(f'{env}-{project_name}-public', region=region)

locking = LockingAPI(f'{env}-{project_name}-locking', region=region)
firehose_log = Firehose(f'{env}-{project_name}', f'{env}-{project_name}-firehose', 'log', region=region)

ses = SESAPI(region=region)
sqs = SQSAPI(f'https://sqs.{region}.amazonaws.com/<aws_account_id>/{env}-queue', region=region)
