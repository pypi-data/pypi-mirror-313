"""
실제로 DOC HTML 을 만들어냄
"""


import os
import time
from typing import List, Optional, Literal
from dataclasses import dataclass
import json
from datetime import datetime


# 현재 실행 중인 스크립트의 전체 경로를 가져옵니다.
script_path = os.path.abspath(__file__)

# 현재 스크립트가 위치한 디렉토리의 경로를 가져옵니다.
directory_path = os.path.dirname(script_path)

# html 파일의 경로를 알아냅니다.
html_path = os.path.join(directory_path, 'api_doc_template')


@dataclass
class APIInfo:
    tags:List[str]
    name:str
    description:str
    body:dict
    headers:dict
    response_body:Optional[dict] = None


class DocMaker:

    def __init__(self, entry_function:any, base_url:str, test_function:any):
        """
        문서화 객체를 초기화합니다.
        :param entry_function: 테스트할 함수 객체입니다. 나중에 test_function 내부에서 호출됩니다.
        :param base_url: API 문서에 사용될 URL 입니다.
        :param api_json_name: json 이 파일로 작성될때의 이름입니다.
        :param test_function: entry_function 을 감싸서 호출하는 함수이고, 안에서 Input 과 Output 을 Wrpping 하는 역할입니다.
        (body, headers, entry_function)->response_body:dict
        """
        self.do_test = False
        self.api_list:List[APIInfo] = []
        self.entry_function = entry_function
        self.test_function = test_function
        self.base_url = base_url
        self.headers = dict()

    def req(self, api_name:str, api_description:str, body:dict, headers:dict, ignore_err=False, api_tags:List[str]=None, run_func:bool=True, mock_response:dict=None)->Optional[dict]:
        # 테스트
        response = None
        if self.do_test and run_func:
            try:
                response = self.test_api(body, headers)
            except Exception as ex:
                if not ignore_err:
                    raise ex
        # 기록
        api_info = APIInfo(
            tags=api_tags,
            name=api_name, description=api_description, body=body, headers=headers
        )
        self.api_list.append(api_info)
        if self.do_test:
            api_info.response_body = response if run_func else mock_response

        return response

    def test_api(self, body, headers):
        """
        API 를 테스트하는데, 오류가 나면 그대로 Raise 합니다.
        """
        response_body = self.test_function(body, headers, self.entry_function)
        return response_body


    def add_header(self, key:str, value_type:Literal["string", "number", "boolean"], default_value:any, description:str, required:bool):
        """
        헤더 컴포넌트를 추가합니다.
        :param key:
        :param value_type:
        :param default_value:
        :param description:
        :param required:
        :return:
        """
        self.headers[f'{key}_header'] = {
                        "in": "header",
                        "name": key,
                        "schema": {
                            "type": value_type,
                            "default": default_value,
                        },
                        "required": required,
                        "description": description
                    }

    def start_test(self):
        # 이 함수를 호출한 시점 이후부터는 TEST 로직 작동 가능
        self.do_test = True

    def end_test(self):
        # 이 함수를 호출한 시점 이후부터는 TEST 로직 작동 가능
        self.do_test = False

    def make_openapi3_json(self, api_json_path):
        """
        APIInfos를 사용하여 Swagger 형식의 JSON API 문서를 생성합니다.
        """
        openapi_doc = {
            "openapi": "3.0.0",
            "info": {
                "title": "Generated API Documentation",
                "description": f"Auto-generated API documentation. {datetime.now()}",
                "version": "1.0.0"
            },
            "servers": [
                {
                    "url": self.base_url
                }
            ],
            "paths": {},
             "components": {
                "parameters": self.headers
                # 다른 컴포넌트 정의 ...
            }
        }

        for idx, api in enumerate(self.api_list):
            path = f"/?n={api.name}"  # 경로
            method = "post"  # 예시 HTTP 메소드

            # Body 파라미터 추가
            body_properties = {}
            for key, value in api.body.items():
                # 파이썬 타입을 OpenAPI 타입으로 변환
                type_name = type(value).__name__
                if type_name == 'str':
                    openapi_type = 'string'
                elif type_name in ['int', 'float']:
                    openapi_type = 'number'
                elif type_name == 'bool':
                    openapi_type = 'boolean'
                else:
                    openapi_type = 'string'  # 기본값

                # 예시 값 설정
                body_properties[key] = {"type": openapi_type, "example": value}

            request_body = {
                "description": "요청 본문",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": body_properties
                        }
                    }
                }
            }

            parameters = [
                {"$ref": f"#/components/parameters/{name}"} for name, _ in self.headers.items()
            ]

            response_example = api.response_body if api.response_body else {}
            responses = {
                "200": {
                    "description": "성공적인 응답",
                    "content": {
                        "application/json": {
                            "example": response_example
                        }
                    }
                }
            }

            openapi_doc["paths"].setdefault(path, {})
            openapi_doc["paths"][path][method] = {
                "summary": api.name,
                "description": api.description,
                'requestBody': request_body,
                'parameters': parameters,
                "responses": responses
            }
            if api.tags:
                openapi_doc['paths'][path][method]['tags'] = api.tags
            # 요청 및 응답 본문 스키마는 APIInfo의 구조에 따라 정의해야 합니다.

        with open(api_json_path, 'w+') as fp:
            json.dump(openapi_doc, fp, indent=4)

        return openapi_doc

    def get_api_list(self)->List[APIInfo]:
        return self.api_list


    @classmethod
    def read_doc_html(cls, api_base_url:str= 'main_api.json', title='API Docs'):
        """
        템플릿 바탕으로 html 파일을 생성해서 반환합니다.
        :return:
        """
        html = '<!DOCTYPE html><html>  <head>    <meta charset="UTF-8">    <meta name="viewport" content="width=device-width, initial-scale=1">    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">    <title>{{title}}</title>    <!-- Redoc 라이브러리 추가 -->  </head>  <body>    <div id="redoc-container"></div>    <script src="https://cdn.jsdelivr.net/npm/redoc@2.0.0-rc.55/bundles/redoc.standalone.min.js"> </script>    <script src="https://cdn.jsdelivr.net/gh/wll8/redoc-try@1.4.9/dist/try.js"></script>    <script>   initTry({        openApi: `{{api_url}}`,        redocOptions: {scrollYOffset: 50},      })    </script>  </body></html>'
        # with open(html_path, 'r') as fp:
        #     html = fp.read()
        html = html.replace('{{api_url}}', f'{api_base_url}?v={int(time.time())}')
        html = html.replace('{{title}}', title)
        return html

    @classmethod
    def read_doc_json(cls, json_file_name:str= 'main_api.json'):
        json_path = os.path.join(directory_path, json_file_name)
        with open(json_path, 'r') as fp:
            json_text = fp.read()
        return json_text


if __name__ == '__main__':
    pass
