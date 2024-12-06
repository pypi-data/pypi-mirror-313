

# AWS Lambda 에 Container 형태로 배포하는 방법

도커(Docker)로 패키징하여 AWS Lambda에 배포하는 방식으로,
기본적인 람다보다 훨씬 더 상세하게 요구사항을 만족시킬수 있음.
셀레니움 같은 크롤링을 지원해야할때 라이브러리 설치 조건을 만족시키기 위해서 사용.

AWS CodeCommit 및 CodeBuild, CodePipeline 를 세팅했다는 가정 하에,
build_spec.yml 파일을 다음과 같이 작성하여 AWS CodeCommit 에 커밋시 
자동으로 ECR 에 이미지를 업로드하고 원하는 Lambda 에 컨테이너 행태로 배포가 되도록 만들 수 있습니다.

> build_spec.yml 파일 구성 (AWS CodeBuild 설정에서 파일명 지정 가능)
```yaml
version: 0.2

env:
  variables:
    AWS_DEFAULT_REGION: ap-northeast-2  # AWS 리전 설정
    IMAGE_REPO_NAME: docker-image-for-lambda  # ECR에 저장할 이미지 이름
    AWS_ACCOUNT_ID: <YOUR_AWS_ACCOUNT_ID>
    LAMBDA_FUNCTION_NAME: docker-lambda

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
      - docker push $REPOSITORY_URI:$IMAGE_TAG  # ECR로 푸시
      - echo Docker image pushed to $REPOSITORY_URI with tag $IMAGE_TAG

      # AWS Lambda에 배포
      - echo Updating Lambda function with new image...
      - aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --image-uri $REPOSITORY_URI:$IMAGE_TAG
      - echo Lambda function $LAMBDA_FUNCTION_NAME updated with image $REPOSITORY_URI:$IMAGE_TAG

artifacts:
  files:
    - '**/*'
  discard-paths: yes



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

# AWS Lambda Runtime Interface Client 설치
RUN pip install --no-cache-dir awslambdaric

# 필요한 라이브러리 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 빌드 키퍼 실행
RUN python build_keeper.py

# Lambda 핸들러 실행 명령어 (app.py 파일의 handler(event, context) 함수를 핸들러로 사용)
CMD ["python", "-m", "awslambdaric", "app.handler"]

```