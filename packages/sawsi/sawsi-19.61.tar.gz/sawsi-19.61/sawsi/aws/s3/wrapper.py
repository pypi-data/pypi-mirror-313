import tempfile
from sawsi.aws import shared
from botocore.exceptions import ClientError


class S3:
    def __init__(self, boto3_session, region=shared.DEFAULT_REGION):
        self.client = boto3_session.client('s3', region_name=region)
        self.resource = boto3_session.resource('s3', region_name=region)
        self.region = region

    def init_bucket(self, bucket_name, acl='private'):
        try:
            self.create_bucket(bucket_name, acl)
        except Exception as ex:
            print(ex)

    def create_bucket(self, bucket_name, acl='private'):
        response = self.client.create_bucket(
            ACL=acl,
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': self.region
            }
        )
        return response

    def upload_binary(self, bucket_name, file_name, binary):
        with tempfile.TemporaryFile() as tmp:
            tmp.write(binary)
            tmp.seek(0)
            response = self.client.upload_fileobj(tmp, bucket_name, file_name)
            return response

    def delete_binary(self, bucket_name, file_name):
        return self.resource.Object(bucket_name, file_name).delete()

    def download_binary(self, bucket_name, file_name):
        with tempfile.NamedTemporaryFile() as data:
            self.client.download_fileobj(bucket_name, file_name, data)
            data.seek(0)
            return data.read()

    def download_file(self, bucket_name, object_key, path):
        return self.client.download_file(bucket_name, object_key, path)

    def upload_file_path(self, bucket_name, upload_path, object_key, content_type, acl="public-read"):
        self.client.upload_file(upload_path, bucket_name, object_key,
                                ExtraArgs={
                                    'ACL': acl,
                                    'ContentType': content_type
                                })

    def delete_bucket(self, bucket_name):
        response = self.client.delete_bucket(
            Bucket=bucket_name
        )
        return response

    def upload_file(self, bucket_name, file_bytes, file_name, content_type='text/html', acl='public-read'):
        """
        파일을 올림, 컨텐츠 타입 고려함
        :param bucket_name:
        :param file_bytes:
        :param file_name:
        :param content_type:
        :param acl:
        :return:
        """
        response = self.client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_bytes,
            ContentType=content_type,
            ACL=acl,
        )
        return response

    def select_object_content(self, bucket_name, object_key, query, input_serialization, output_serialization):
        response = self.client.select_object_content(
            Bucket=bucket_name,
            Key=object_key,
            RequestProgress={
                'Enabled': True
            },
            Expression=query,
            ExpressionType='SQL',
            InputSerialization=input_serialization,
            OutputSerialization=output_serialization,
        )
        return response


    def list_objects_v2(self, bucket_name, prefix, limit, start_after=None, continuation_token=None):
        request_payload = {
            'Bucket': bucket_name,
            'Prefix': prefix,
            'MaxKeys': limit
        }
        if continuation_token:
            request_payload['ContinuationToken'] = continuation_token
        if start_after:
            request_payload['StartAfter'] = start_after

        response = self.client.list_objects_v2(**request_payload)
        return response

    def create_presigned_url(self, bucket_name, client_method, object_name, content_type, acl='private', expiration=3600):
        """S3 버킷에 대한 사전 서명된 URL을 생성합니다.
        # 사용 예:
        # bucket_name = 'your-bucket-name'
        # object_name = 'your/object/key.jpg'
        # content_type = 'image/jpeg'
        # acl = 'public-read' or 'private'
        # url = create_presigned_url(bucket_name, object_name, content_type)
        # print(url)
        """
        s3_client = self.client
        params = {
            'Bucket': bucket_name,
            'Key': object_name,
        }
        if content_type:
            params['ContentType'] = content_type
        if acl:
            params['ACL'] = acl
        response = s3_client.generate_presigned_url(
            client_method,  # 'put_object'
            Params=params,
            ExpiresIn=expiration,
        )
        return response

    def head_object(self, bucket_name: str, key: str):
        """
        S3 버킷에서 특정 키가 존재하는지 확인합니다.
        :param bucket_name: S3 버킷 이름
        :param key: 확인하고자 하는 키 이름 (파일 이름)
        :return: 키가 존재하면 True, 그렇지 않으면 False를 반환
        """
        try:
            return self.client.head_object(Bucket=bucket_name, Key=key)
        except Exception as ex:
            # ClientError 발생 시, 에러 코드를 확인하여 404 에러(Not Found)인 경우 False 반환
            return None

