# SAWSI - Simple AWS Interface

**간략한 설명**: 
AWS 의 boto3 를 Wrapping 하여 손쉽게 DynamoDB, S3, SecretManager 등의 서비스를 활용할 수 있도록 만든 라이브러리입니다.

또한 API 배포 및 테스팅 자동화, S3의 경우 파일을 올리면 URL로 자동으로 뽑아주는 등의 유용한 기능들이 포함되어 있습니다.
추가적으로 AWS API Gateway 와 Lambda 의 연결을 원활하게 해주는 핸들러 유틸이 포함되어 있습니다.
## 시작하기

```bash
pip install sawsi
# 설치 완료 후 스크립트를 실행하고, 원하는 프로젝트명과 앱 이름을 입력합니다.
awsi init test_project test_app_user
# init 이후에는 add 명령어를 통해 앱을 추가할 수 있습니다.
awsi add test_app_admin
# 명령어 실행 이후 프로젝트 디렉터리에 파일이 세팅된것을 확인하실 수 있습니다.
# 프로젝트 내부에 사용자 대상 코드, Admin 관리자 코드를 함께 관리하는 구성을 추천합니다.
```
프로젝트와 앱을 생성하면, 기본적으로 필요한 디렉터리 구조와 샘플 파일들이 생성됩니다.
- app 이름으로 폴더가 생성되며, 내부에 샘플 코드들이 탑재됩니다.
- "aws_iam_policy_dev|prod.json" 파일이 IAM 정책 생성시 활용할 수 있게끔 생성됩니다.
- AWS CodePipeline > CodeBuild 에 활용할 수 있는 "buildspec-dev|prod.yml" 파일이 생성됩니다.

#### 프로젝트가 잘 세팅되었다면 아래와 같은 순서로, 코드와 연결되는 AWS 인프라를 초기 세팅해주어야 배포 자동화가 가능합니다.
1. AWS에서 기본적으로 사용될 Lambda 함수를 생성해야합니다.
   - Lambda 역할 (Role) 생성시 "aws_iam_policy_dev|prod.json" 파일의 정책을 복사하면 권한세팅을 빠르게 마칠 수 있습니다
2. Lambda 와 연결될 API Gateway 를 세팅해줍니다.
3. 이외 CloudWatch(Event Scheduler), SQS 등 필요하다면 프로젝트 구성상 Lambda 와 연결되어야 하는 구성을 추가로 세팅해줍니다.
4. Github이나 AWS CodeCommit 등을 레포로 사용한다면, CI/CD를 위해 각 환경별 (dev, prod) CodePipeline 을 세팅합니다. (CodeDeploy 구성은 건너뛰어주세요)
    1. AWS CodePipeline 에서 안내하는대로 파이프라인을 세팅하면서
   2. 빌드 이미지는 Amazon Linux x86 최신으로 지정하고
   3. buildspec-dev|prod.yml 을 각각 세팅해줍니다
   4. 완료하면 총 2개의 CodePipeline 이 생성됩니다. 

## 주의사항
DynamoDB 의 경우 Pure 한 구성이 아닌, ORM 형식으로 데이터 구조를 변형하여 저장하기 때문에, 기존 사용하던 DB에 덮어 사용시 충돌이 생길 수 있으니 새로운 DDB 객체를 생성하여 사용함을 권장드립니다.

## 프로젝트 사용방법

### 주요 SAWSI API 사용 방법

#### 1. DynamoDB
완전 관리형 NoSQL 데이터베이스 서비스로, 빠른 성능과 유연성을 제공합니다. 데이터 항목과 문서를 저장하고 검색하는 데 사용됩니다. 
* 사용 예시: 사용자 정보, 상품 카탈로그, 세션 저장소 등 다양한 데이터 저장 용도로 사용할 수 있습니다.

```python
from sawsi.aws.dynamodb.api import DynamoDBAPI

dynamodb_api = DynamoDBAPI(group_name='my-project-name')
table_name = 'my_user_table'
# 테이블 생성
dynamodb_api.create_table(table_name)
# 아이템 삽입
item = {'id': '1', 'name': 'John Doe'}
dynamodb_api.put_item(table_name, item)
# 아이템 조회
item = dynamodb_api.get_item(table_name, '1')
print(item)
```

#### 2. Kinesis Firehose
실시간으로 데이터 스트림을 캡처하고 자동으로 S3, Redshift, Elasticsearch 등의 AWS 서비스로 로드할 수 있게 해주는 서비스입니다.
* 사용 예시: 실시간 로그 또는 이벤트 데이터를 S3에 저장하거나 실시간 분석을 위해 Elasticsearch로 전송합니다.


```python
from sawsi.aws.firehose.api import Firehose

firehose_api = Firehose(delivery_stream_name='my-delivery-stream', bucket_name='my-s3-bucket', object_key_prefix='my-data')
# Firehose 스트림 초기화
firehose_api.init()
# 데이터 레코드 전송
data = '{"user_id": "TEST_USER_ID", "transactions": [{...}, ...]}'
firehose_api.put_record(data)

# 저장 완료 후 5분 정도 뒤에, 저장된 로그를 읽을 수 있음
cursor = None  # 저장된 cursor 뒤의 페이지부터 읽을 수 있음
gen = firehose_api.generate_log_json_list_and_key(key_start_after=cursor)
    for log_json_list, cur_cursor in gen:
        for log_json in log_json_list:
            user_id = log_json['user_id']
            transactions = log_json['transactions']
```

#### 3. Locking with DynamoDB
DynamoDB를 활용하여 분산 락 관리 시스템을 구현할 수 있습니다. 여러 애플리케이션 인스턴스가 동시에 같은 리소스에 접근하는 것을 방지합니다.
* 사용 예시: 여러 서버가 동일한 작업을 수행하지 않도록 하거나, 중복 실행을 방지하기 위해 리소스 락을 구현합니다.
```python
from sawsi.aws.locking.api import LockingAPI
import time

locking_api = LockingAPI(table_name='my-lock-table')
# 테이블 초기화 (이미 생성되어 있다면 생략 가능)
locking_api.init_table()

object_key = 'unique-resource-identifier'
try:
    # Lock 획득 시도
    with locking_api.lock(object_key) as lock:
        # Lock이 성공적으로 획득되면, 여기에 리소스를 안전하게 사용하는 코드를 작성
        print(f"Lock acquired for {object_key}. Doing work.")
        time.sleep(10)  # 대표적인 작업을 시뮬레이션하기 위한 대기 시간
        # 작업 완료 후 Lock이 자동으로 해제됩니다.
except RuntimeError as e:
    print(f"Failed to acquire lock for {object_key}: {e}")
```

#### 4. S3
안전하고 확장 가능한 클라우드 스토리지 서비스입니다. 웹사이트 콘텐츠, 백업, 아카이브 등 다양한 데이터를 저장할 수 있습니다.
* 사용 예시: 정적 웹사이트 호스팅, 데이터 백업, 빅데이터 분석을 위한 데이터 레이크로 사용합니다.

```python
from sawsi.aws.s3.api import S3API

s3_api = S3API(bucket_name='my-s3-bucket')
# S3 버킷 초기화, 이때 버킷이 실제로 생성 됨.
s3_api.init_s3_bucket()
# 파일 업로드
file_name = 'example.txt'
file_content = b'Hello, S3!'
s3_api.upload_binary(file_name, file_content)
url = s3_api.upload_file_and_return_url(file_content, 'txt', 'text/plain', use_accelerate=True, forced_file_id='not_a_random_gen_id')
# 파일 다운로드
downloaded_content = s3_api.download_binary(file_name)
print(downloaded_content)
```

#### 5. Secrets Manager
암호화된 비밀번호, API 키, 기타 중요한 정보를 안전하게 저장하고 관리할 수 있는 서비스입니다.
* 사용 예시: 데이터베이스 비밀번호, API 키 등의 비밀 정보를 애플리케이션에 안전하게 제공합니다.

```python
from sawsi.aws.secrets_manager.api import SecretManagerAPI

secrets_api = SecretManagerAPI(secret_name='my-secret')
# 비밀값 조회
db_password = secrets_api.get_secret_value('dbPassword')
print(f"Database password: {db_password}")
```

#### 6. SES (Simple Email Service)
이메일을 보내고 받을 수 있게 해주는 비용 효율적인 클라우드 기반 서비스입니다.
* 사용 예시: 애플리케이션에서 사용자에게 이메일 알림을 보내거나, 마케팅 이메일을 대량으로 발송합니다.

```python
from sawsi.aws.ses.api import SESAPI

ses_api = SESAPI()
# 이메일 보내기
sender = 'sender@example.com'
recipient = 'recipient@example.com'
subject = 'Test Email'
body_text = 'Hello, this is a test email.'
body_html = '<html><body><h1>Hello, this is a test email.</h1></body></html>'
ses_api.send_email(sender, recipient, subject, body_text, body_html)
```

#### 7. SMS (Simple Notification Service)
텍스트 메시지(SMS)를 전송할 수 있는 완전 관리형 통신 서비스입니다.
* 사용 예시: 인증 코드 전송, 알림 메시지 발송 등 사용자 휴대폰으로 직접 메시지를 전송합니다.

```python
from sawsi.aws.sms.api import SMSAPI

sms_api = SMSAPI(region_name='us-east-1')
# SMS 전송
phone_number = '+1234567890'
message = 'This is a test SMS message.'
sms_api.send_sms(phone_number, message)
```

#### 8. SQS (Simple Queue Service)
메시지 큐 서비스로, 서로 다른 컴포넌트, 시스템, 애플리케이션 간에 메시지를 전송하고 저장할 수 있습니다.
* 사용 예시: 마이크로서비스, 분산 시스템 간의 비동기 통신, 작업 큐 관리에 사용됩니다.
이러한 서비스들은 AWS의 다양한 클라우드 기반 기능을 제공하여, 애플리케이션의 확장성, 안정성, 보안을 향상시키는 데 도움을 줍니다.

```python
from sawsi.aws.sqs.api import SQSAPI

sqs_api = SQSAPI(queue_url='https://sqs.us-east-1.amazonaws.com/123456789012/my-queue')
# 메시지 보내기
message_body = '{"cmd": "test_message"}'
sqs_api.send_message(message_body)
```

## 추천 사용 방법
프로젝트 생성시 만들어지는 api.py 파일 내부에 해당 API 들을 통해
환경별로 리소스를 생성하고 관리하는 것을 추천합니다.

```python
import os

project_name = '{{project}}'
env = os.getenv('env')

secret_manager: SecretManagerAPI = SecretManagerAPI(f'{env}/{project_name}', region=region)
dynamo = DynamoDBAPI(f'{env}-{project_name}', region=region)
s3_public = S3API(f'{env}-{project_name}-public', region=region)
```
위 api.py 를 다른 파일에서 레퍼런스하여 사용, (이렇게 구성하고 호출하면, 호출부에서는 개발환경에 대한 구분 없이 쉽게 사용 가능합니다.)
```python
import api
value = api.secret_manager.get_secret_value('some_value')
print(value)
```


"**sawsi init project_name app_name**" 명령어를 통해 
앱디렉토리/aws_handler.py 파일이 아래와 같이 생성되며,
개발자가 AWS 콘솔에서 해당 함수와 API Gateway 를 트리거로 연결시켜주면,
바로 가용할 수 있는 API가 배포됩니다.
```python
from sawsi.shared import error_util
from sawsi.shared import handler_util

# 아래 핸들러는 share.error_util.AppError 에러가 발생할시에, 자동으로
# 에러를 response 객체에 담아 코드와 메시지로 구분하여 전송합니다.
@handler_util.aws_handler_wrapper(
    error_receiver=lambda errmsg: print(errmsg),  # 이 Lambda 함수를 슬랙 Webhook 등으로 대체하면 에러 발생시 모니터링이 가능합니다.
    content_type='application/json',  # 기본적으로 JSON 타입을 반환합니다.
    use_traceback=True,  # 에러 발생시 상세 값을 응답에 전달할지 유무입니다.
)
def some_api_aws_lambda_handler(event, context):
    """
    AWS LAMBDA에서 API Gateway 를 통해 콜한 경우
    """
    # API Gateway 로부터 Lambda 에 요청이 들어오면 다음과 같이 body 와 headers 를 분리하여 dict 형태로 반환합니다.
    body = handler_util.get_body(event, context)
    headers = handler_util.get_headers(event, context)
    
    # 아래부터는 사용자가 직접 응용하여 핸들러를 구성, 다른 함수들로 라우팅합니다.
    cmd = body['cmd']
    if cmd == 'member.request_login':
        import member
        return member.request_login(
            mid=body['mid'],
            mpw=body['pwd'],
        )
    
    # 핸들러 CMD 에 해당하는 CMD 값이 없을 경우 에러 발생
    raise error_util.SYSTEM_NO_SUCH_CMD
```


###  HighLevel DynamoDB ORM 사용
PyDantic BaseModel 를 기반으로 한 ORM 사용 방법입니다.
각 메소드 실행시 실제 DB에 저장됩니다.
```python
import api
from sawsi.model.base import DynamoModel


class User(DynamoModel):
    __dynamo__ = api.dynamo  # ORM 을 위해 DynamoDB 와 연결하는 부분
    _table = 'user'
    _indexes = [
      ('name', None)
    ]
    name:str

# Usage
user = User(name='Kim')

# Create
user.put(can_overwrite=True)

# Update
user.name = 'Lee'
user.update()

# Query as generator
users = User.generate(pk_field='name', pk_value='Kim')
for user in users:
   print(user.id, user.crt, user.name)

# Query as list of dict
user_datas, end_key = User.query(pk_field='name', pk_value='Kim', start_key=None)
for user_data in user_datas:
   print(user_data['id'], user_data['crt'], user_data['name'])

# Delete
user.delete()
```


DynamoFDBAPI 의 apply_partition_map 기능 사용
* 이 기능을 통해, 파티션 구성을 한번에 마이그레이션할 수 있습니다. 예를 들면 개발환경에서 쓰던 구성을 한번에 프로덕션으로 가져갈 수 있습니다.
* 배포 전에 작동하는 스크립트를 구현해놓고 사용하시는것을 권장합니다.
* 주의: One Big Table 구조를 사용할 수 없는 환경에서는 DynamoDBAPI 를 추천드립니다.
```python
# DynamoFDBAPI 객체 생성
from sawsi.aws.dynamodb.api import DynamoFDBAPI

fdb_api = DynamoFDBAPI('<your_table_name>')

# 파티션 맵 정의
fdb_partition_map = {
    'your_partition_name': {
        'pk': '<primary_key_name>',
        'sk': '<sort_key_name>',
        'uks': ['<optional_unique_key1>', '<optional_unique_key2>'],
        'indexes': [
            {'pk': '<primary_key_name>', 'sk': '<sort_key_name>'},
            {'pk': '<another_primary_key_name>', 'sk': '<another_sort_key_name>'},
            # ... 여러 인덱스 정의
        ]
    },
    # ... 다른 파티션 정의
}

# 파티션 맵 적용
fdb_api.apply_partition_map(fdb_partition_map)
```


배포 자동화 기능 사용
AWS CodeCommit 및 CodeBuild, CodePipeline 를 세팅했다는 가정 하에,
build_spec.yml 파일을 다음과 같이 작성하여 AWS CodeCommit 에 커밋시 
자동으로 원하는 Lambda 에 배포가 되도록 만들 수 있습니다.
> build_spec.yml 파일 구성 (AWS CodeBuild 설정에서 파일명 지정 가능)
```yaml
version: 0.2
# AWS Codebuild 환경 > 이미지 구성 > amazon/aws-lambda-python:3.11
# https://hub.docker.com/r/amazon/aws-lambda-python/tags 참고해서 정할 것

env:
  variables:
    ARN_BASE: "arn:aws:lambda:us-west-1:{ARN_NUMBER}"
    # 아래에 배포할 Lambda 속성들을 리스트업합니다.
    LAMBDAS: |
      [
        {"name": "dev_usa_serverless_main", "handler": "l0_endpoint.main.handler"},
        {"name": "dev_usa_serverless_scheduler", "handler": "l0_endpoint.scheduler.handler"},
        {"name": "dev_usa_serverless_admin", "handler": "l0_endpoint.admin.handler"},
        {"name": "dev_usa_serverless_plaid_webhook", "handler": "l0_endpoint.plaid_webhook.handler"},
        {"name": "dev_usa_serverless_queue_worker", "handler": "l0_endpoint.queue_worker.handler"}
      ]
    # 필요하면 추가..
    RUNTIME: "python3.11"
    MEM_SIZE: "2048"
    S3_BUCKET: "dev-build"


phases:
  pre_build:
    commands:
      - export DATE=$(date +%Y%m%d%H%M%S)
  install:
    commands:
      - echo Installing required tools...
      - yum install unzip -y
      - yum install -y zip
      - yum install -y jq
      # x86_64 혹은 arm 중에 선택합니다.
      - curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#      - curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
      - mkdir awscliv2
      - unzip awscliv2.zip -d awscliv2
      - ./awscliv2/aws/install
      - aws --version
      - rm -rf awscliv2
      - rm -rf awscliv2.zip

  build:
    commands:
      - echo Build started on `date`
      - echo Installing requirements.txt...
      - pip install -r requirements.txt.txt -t .
      - echo Zipping the project...
      - zip -r function.zip .
      - cp function.zip ../function.zip
      - python3 build_keeper.py
      - echo Uploading to S3...
      - aws s3 cp function.zip s3://$S3_BUCKET/$DATE/function.zip

  post_build:
     commands:
       - |
          for row in $(echo "${LAMBDAS}" | jq -r '.[] | @base64'); do
            _jq() {
              echo ${row} | base64 --decode | jq -r ${1}
            }
    
            LAMBDA_FUNCTION_NAME=$(_jq '.name')
            HANDLER=$(_jq '.handler')
            
            sleep 1
            aws lambda update-function-configuration --function-name $LAMBDA_FUNCTION_NAME --runtime $RUNTIME --handler $HANDLER --memory-size $MEM_SIZE --description DeployByCodebuild 
            sleep 1
            aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --s3-bucket $S3_BUCKET --s3-key $DATE/function.zip
            sleep 1
            aws lambda publish-version --function-name $LAMBDA_FUNCTION_NAME
          done

artifacts:
  files:
    - function.zip
  discard-paths: yes

```



## AWS CodeCommit 저장소 Clone 방법

AWS CodeCommit은 AWS에서 제공하는 관리형 소스 컨트롤 서비스로, Git을 사용하여 리포지토리를 클론하고 관리할 수 있습니다. CodeCommit 리포지토리를 클론하기 위해서는 몇 가지 사전 준비와 단계를 따라야 합니다.

### 사전 준비
* AWS CLI 설치 및 구성: AWS CLI가 설치되어 있지 않다면 설치하고, aws configure 명령을 사용하여 액세스 키 ID, 비밀 액세스 키, 기본 리전 등을 구성합니다.
* IAM 사용자 권한: CodeCommit 리포지토리에 액세스할 수 있는 IAM 사용자 또는 역할이 필요합니다. 이 사용자 또는 역할에는 CodeCommit 리포지토리에 대한 액세스 권한이 부여되어 있어야 합니다.
* Git 설치: 로컬 시스템에 Git이 설치되어 있어야 합니다.
* CodeCommit 리포지토리 클론하기
* 리포지토리의 HTTPS URL 찾기: AWS Management Console에서 CodeCommit 서비스로 이동하여 클론하려는 리포지토리를 선택합니다. 리포지토리의 세부 정보 페이지에서 'Clone URL' 섹션을 찾아 HTTPS URL을 복사합니다.

### Git Credential Helper 구성
AWS CLI의 Git Credential Helper를 사용하여 인증을 구성합니다. 이는 AWS 자격 증명을 사용하여 CodeCommit 리포지토리에 액세스할 수 있게 해줍니다. 터미널에서 다음 명령을 실행하여 구성합니다:
```bash
git config --global credential.helper '!aws codecommit credential-helper $@'
git config --global credential.UseHttpPath true
```
### 리포지토리 클론
이제 Git을 사용하여 리포지토리를 클론할 수 있습니다. 터미널에서 다음과 같은 명령을 사용합니다:

```bash
git clone https://git-codecommit.[리전].amazonaws.com/v1/repos/[리포지토리 이름]
```
[리전]은 리포지토리가 호스팅되는 AWS 리전(예: us-east-1)으로 교체하고, [리포지토리 이름]은 클론하려는 리포지토리의 이름으로 교체합니다.

