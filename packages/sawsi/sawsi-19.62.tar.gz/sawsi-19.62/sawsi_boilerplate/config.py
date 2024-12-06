import os

# 환경변수
env = os.getenv('env', 'dev')
region = 'ap-northeast-2'

# 빌드 상태인지 확인할 수 있는 변수, 빌드가 실행될때만 True로 변경됨.
build = False