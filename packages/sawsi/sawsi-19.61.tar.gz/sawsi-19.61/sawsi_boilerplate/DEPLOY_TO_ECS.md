

# AWS ECS 에 Container 형태로 배포하는 방법 

도커(Docker)를 이용한 AWS ECS에 배포 (람다 아님)
AWS CodeCommit 및 CodeBuild, CodePipeline 를 세팅했다는 가정 하에,
build_spec.yml 파일을 다음과 같이 작성하여 AWS CodeCommit 에 커밋시 
자동으로 ECR 에 이미지를 업로드하고 원하는 ECS Service 에 컨테이너 행태로 배포가 되도록 만들 수 있습니다.

> build_spec.yml 파일 구성 (AWS CodeBuild 설정에서 파일명 지정 가능)
```yaml
version: 0.2

env:
  variables:
    AWS_DEFAULT_REGION: ap-northeast-2  # AWS 리전 설정
    IMAGE_REPO_NAME: sample-docker-image  # ECR에 저장할 이미지 이름
    AWS_ACCOUNT_ID: <YOUR_AWS_ACCOUNT_ID>
    ECS_CLUSTER_NAME: ecs-cluster
    ECS_SERVICE_NAME: ecs-service-main

phases:
  pre_build:
    commands:
      - REPOSITORY_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $REPOSITORY_URI
      - IMAGE_TAG=$(date '+%Y%m%d%H%M%S')  # 현재 날짜와 시간으로 이미지 태그 설정
      - echo "Docker image will be tagged as $REPOSITORY_URI:$IMAGE_TAG"

  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build --build-arg AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION --build-arg AWS_CONTAINER_CREDENTIALS_RELATIVE_URI=$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI -t $IMAGE_REPO_NAME:$IMAGE_TAG .  # 이미지 이름과 태그 지정
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $REPOSITORY_URI:$IMAGE_TAG  # 이미지 태그를 ECR 레포지토리로 재지정
      - echo Docker image built and tagged as $REPOSITORY_URI:$IMAGE_TAG

  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image...
      - docker push $REPOSITORY_URI:$IMAGE_TAG  # ECR로 버전 태그 푸시
      - echo Docker image pushed to $REPOSITORY_URI with tag $IMAGE_TAG

      # 태스크 정의 업데이트
      - echo Updating ECS service with the new image...
      - |
        NEW_TASK_DEFINITION=$(jq --arg IMAGE "$REPOSITORY_URI:$IMAGE_TAG" '.containerDefinitions[0].image = $IMAGE' task-define.json)
        NEW_TASK_DEFINITION_ARN=$(aws ecs register-task-definition --cli-input-json "$NEW_TASK_DEFINITION" --output text --query 'taskDefinition.taskDefinitionArn')

      # 서비스 업데이트
      - aws ecs update-service --cluster $ECS_CLUSTER_NAME --service $ECS_SERVICE_NAME --task-definition $NEW_TASK_DEFINITION_ARN --force-new-deployment
      - echo ECS service updated successfully

artifacts:
  files:
    - '**/*'
  discard-paths: yes


```

> task-define.json 파일 (위 build_spec.yml 파일과 동일 경로에 위치시켜주세요)
기본적인 Task 에 대한 정보를 담고 있으며, 원하는 사양으로 수정해야합니다.

```json

{
    "family": "main-task",
    "containerDefinitions": [
        {
            "name": "main",
            "image": "<YOUR_ECR_IMAGE_URI>",
            "cpu": 0,
            "portMappings": [
                {
                    "name": "main",
                    "containerPort": 8000,
                    "hostPort": 8000,
                    "protocol": "tcp",
                    "appProtocol": "http"
                }
            ],
            "essential": true,
            "environment": [
                {
                    "name": "env",
                    "value": "dev"
                }
            ],
            "mountPoints": [],
            "volumesFrom": [],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/main-task",
                    "mode": "non-blocking",
                    "awslogs-create-group": "true",
                    "max-buffer-size": "25m",
                    "awslogs-region": "ap-northeast-2",
                    "awslogs-stream-prefix": "ecs"
                },
                "secretOptions": []
            },
            "systemControls": []
        }
    ],
    "taskRoleArn": "arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:role/ecsTaskExecutionRole",
    "executionRoleArn": "arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:role/ecsTaskExecutionRole",
    "networkMode": "awsvpc",
    "requiresCompatibilities": [
        "FARGATE"
    ],
    "cpu": "1024",
    "memory": "2048",
    "ephemeralStorage": {
        "sizeInGiB": 50
    },
    "runtimePlatform": {
        "cpuArchitecture": "ARM64",
        "operatingSystemFamily": "LINUX"
    }
}

```

> Dockerfile 파일 (위 build_spec.yml 파일과 동일 경로에 위치시켜주세요)

```Dockerfile

# 베이스 이미지 선택
FROM python:3.12

# Codebuild 의 자격증명을 docker 에서 그대로 사용하기 위함
ARG AWS_DEFAULT_REGION
ARG AWS_CONTAINER_CREDENTIALS_RELATIVE_URI

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 필요한 라이브러리 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

RUN python build_keeper.py

# 서버 실행
CMD ["uvicorn", "main.ec2_server:app", "--host", "0.0.0.0", "--port", "8000"]

```