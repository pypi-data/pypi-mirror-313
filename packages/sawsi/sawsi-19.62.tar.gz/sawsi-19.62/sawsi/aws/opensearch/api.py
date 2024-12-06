import json

import urllib3
from sawsi.aws import shared
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from sawsi.shared.dict_util import convert_dynamodb_document_to_dict
from typing import Literal

http = urllib3.PoolManager()

service = 'es'

class OpenSearchAPI:
    """
    API Gateway Management API
    """
    def __init__(self, domain_endpoint_url, credentials=None, region=shared.DEFAULT_REGION):
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
        self.domain_endpoint_url = domain_endpoint_url
        if self.domain_endpoint_url.endswith('/'):
            # 뒤에 슬레쉬 짜름
            self.domain_endpoint_url = self.domain_endpoint_url[:-1]
        self.region = region

    def _http_request(self, method, url, body, region):
        signed_request = self._sign_request(method, url, body=body, region=region)
        response = http.request(
            method,
            signed_request.url,
            body=signed_request.body,
            headers=signed_request.headers
        )
        # status = response.status
        # response_body = response.data.decode('utf-8')
        return response

    def _sign_request(self, method, url, body, region):
        # BOTO3 서명
        credentials = self.boto3_session.get_credentials()
        headers = {'Content-Type': 'application/json'}
        request = AWSRequest(method=method, url=url, data=body, headers=headers)
        SigV4Auth(credentials, service, region).add_auth(request)
        return request.prepare()

    def run(self, method: Literal["GET", "POST", "PUT", "DELETE"], path, body):
        url = f'{self.domain_endpoint_url}/{path}'
        response = self._http_request(method, url, body, region=self.region)
        return response

    def put_document(self, index_name: str, doc_id: str, document: dict):
        path = f"{index_name}/_doc/{doc_id}"
        doc_body = convert_dynamodb_document_to_dict(document)
        doc_body = json.dumps(doc_body)
        response = self.run('PUT', path, doc_body)
        return response

    def delete_document(self, index_name: str, doc_id: str):
        path = f"{index_name}/_doc/{doc_id}"
        response = self.run('DELETE', path, None)
        return response

    def bulk_put_documents(self, index_name: str, documents: dict[str, dict]):
        """
        여러 문서를 한번에 인덱싱하는 메서드
        :param index_name: 인덱스 이름
        :param documents: {"doc_id1": document1, "doc_id2": document2, ...}
        """
        bulk_data = ""
        for doc_id, document in documents.items():
            doc_body = convert_dynamodb_document_to_dict(document)
            bulk_data += json.dumps({"index": {"_index": index_name, "_id": doc_id}}) + "\n"
            bulk_data += json.dumps(doc_body) + "\n"

        response = self.run('POST', '_bulk', bulk_data)
        return response

    def bulk_delete_documents(self, index_name: str, doc_ids: list):
        """
        여러 문서를 한번에 삭제하는 메서드
        :param index_name: 인덱스 이름
        :param doc_ids: 삭제할 문서의 ID 리스트
        """
        bulk_data = ""
        for doc_id in doc_ids:
            bulk_data += json.dumps({"delete": {"_index": index_name, "_id": doc_id}}) + "\n"

        response = self.run('POST', '_bulk', bulk_data)
        return response
