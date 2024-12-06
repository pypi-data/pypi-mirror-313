"""
Main API 를 테스트하고, API Docs 로 뽑을수 있게 지원
"""
import json
import api
import config
from sawsi.api_doc import doc_generator
from {{app}} import aws_handler


# 개발용만 배포합니다.
base_url = 'https://<YOUR_APP_API_GATEWAY_BASE_URL>'

# API 문서 html 파일이 업로드 될 S3 경로입니다.
dev_app_api_doc_s3 = api.S3API('dev-{{app}}-api-doc', region=config.region)
dev_app_api_doc_s3.init_s3_bucket(acl='public')


def _test_function(body, headers, entry_function):
    # 테스트용 함수
    event = {
        'body': json.dumps(body),
        'headers': headers,
    }
    context = {}
    response = entry_function(event, context)
    body_json = response['body']
    body = json.loads(body_json)
    if body['rslt_cd'] != 'A00000':
        raise Exception(str(body))
    return body


def make_api_doc():
    config.build = True
    doc = doc_generator.DocMaker(aws_handler.handler, base_url=base_url, test_function=_test_function)

    doc.add_header('session_id', 'string', None, '로그인 함수로 발급되는 session_id 값', False)
    doc.add_header('Connection', 'string', 'keep-alive', '고정', False)
    doc.add_header('Accept-Encoding', 'string', 'gzip, deflate, br', '고정', False)
    doc.add_header('Accept', 'string', '*/*', '고정', False)
    doc.add_header('User-Agent', 'string',  'Client', '고정', False)
    doc.add_header('Content-Type', 'string', 'application/json', '고정', False)

    headers = {
        'session_id': None,
        'otp_code': None,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*',
        'User-Agent': 'API-TEST-Python',
        'Content-Type': 'application/json'
    }
    doc.start_test()

    # 테스트와 동시에 문서를 생성합니다.
    body = doc.req(
        api_tags=['인증'],
        api_name='로그인 단계',
        api_description='Initial step of admin login',
        body={
            'cmd': '{{app}}.controller.sample_login.login',
            'email': 'test@gmail.co',  # Replace with a test email
            'password': 'PasswordForTest1234'  # Replace with a test password
        },
        headers=headers,
    )

    """
    아래에 다른 테스트 및 API DOC 생성용 코드들 삽입하세요.
    """

    # 로그인시에 발급 받은 세션 ID를 받아오는 부분
    session_id = body['session_id']
    headers['session_id'] = session_id


    # 아래부터는 API 문서 생성부
    doc.end_test()
    _upload_api_doc(doc)


def _upload_api_doc(doc: doc_generator.DocMaker):
    file_name = '{{app}}_api'
    doc_dict = doc.make_openapi3_json(f'{file_name}.json')
    doc_json = json.dumps(doc_dict)
    doc_json_enc = doc_json.encode('utf-8')
    # JSON 파일 먼저 업로드
    main_api_json_url = dev_app_api_doc_s3.upload_file_and_return_url(
        file_bytes=doc_json_enc, extension='json', content_type='application/json', forced_file_id=f'{file_name}.json'
    )
    doc_html = doc.read_doc_html(
        main_api_json_url, '{{app}} API Docs'
    )
    doc_html_enc = doc_html.encode('utf-8')
    # 이후에 HTML 파일 업로드
    app_api_html_url = dev_app_api_doc_s3.upload_file_and_return_url(
        file_bytes=doc_html_enc, extension='html', content_type='text/html', forced_file_id=f'{file_name}.html',
    )
    print('api_html_url:', app_api_html_url)
    return app_api_html_url


if __name__ == '__main__':
    make_api_doc()

