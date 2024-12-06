

# AWS Lambda 에 Python 런타임으로 배포하는 방법

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
