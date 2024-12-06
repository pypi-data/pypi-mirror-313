import time
import botocore
import botocore.client
from boto3.dynamodb.conditions import Key, Attr
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from concurrent.futures import ThreadPoolExecutor
from typing import Literal, Dict, List, Optional, Any
from botocore.exceptions import ClientError
from sawsi.aws.dynamodb.util import convert_if_number_to_decimal
from decimal import Decimal


type_deserializer = TypeDeserializer()
type_serializer = TypeSerializer()



def decode_dict(dict_obj):
    def cast_number(v):
        if isinstance(v, dict):
            return decode_dict(v)
        if isinstance(v, list):
            return decode_dict(v)
        if isinstance(v, float):
            return Decimal(str(v))
        else:
            return v

    if isinstance(dict_obj, dict):
        return {k: cast_number(v) for k, v in dict_obj.items()}
    elif isinstance(dict_obj, list):
        return [cast_number(v) for v in dict_obj]
    else:
        return dict_obj


def divide_chunks(l, n):
    """
    입력된 리스트 l 을 n 개씩 갖도록 split
    :param l:
    :param n:
    :return:
    """
    # looping till length l
    if isinstance(l, list):
        for i in range(0, len(l), n):
            yield l[i:i + n]
    elif isinstance(l, dict):
        items = list(l.items())
        for i in range(0, len(items), n):
            chunks = items[i: i+n]
            dic = {}
            for key, value in chunks:
                dic[key] = value
            yield dic


class DynamoFDB:
    def __init__(self, boto3_session, table_name, region='us-west-2'):
        dynamo_config = botocore.client.Config(max_pool_connections=100)
        self.client = boto3_session.client('dynamodb', config=dynamo_config, region_name=region)
        self.resource = boto3_session.resource('dynamodb', config=dynamo_config, region_name=region)
        self.table_cache = {}
        self.table_name = f'{table_name}'

    def init_fdb_table(self):
        self.create_fdb_table(self.table_name)
        # self.create_fdb_partition_index(self.table_name)

    def create_fdb_table(self, table_name):
        """
        fdb 용 테이블 생성문입니다.
        :param table_name:
        :return:
        """
        try:
            response = self.client.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': '_pk',
                        'AttributeType': 'S'
                    }, {
                        'AttributeName': '_sk',
                        'AttributeType': 'S'
                    }
                ],
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': '_pk',
                        'KeyType': 'HASH'
                    }, {
                        'AttributeName': '_sk',
                        'KeyType': 'RANGE'
                    },
                ],
                BillingMode='PAY_PER_REQUEST',
                StreamSpecification={
                    'StreamEnabled': True,
                    'StreamViewType': 'NEW_AND_OLD_IMAGES'
                },
            )
            print('CREATING DB TABLE...')
            self.client.get_waiter('table_exists').wait(TableName=table_name)
            return response
        except Exception as ex:
            print(ex)
            return True

    def create_fdb_partition_index(self, table_name, index_name, pk_name, sk_name):
        """
        fdb 용 파티션 쿼리 전용 인덱스 생성문입니다.
        :param table_name:
        :return:
        """
        try:
            response = self.client.update_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': pk_name,
                        'AttributeType': 'S'
                    }, {
                        'AttributeName': sk_name,
                        'AttributeType': 'S'
                    }
                ],
                TableName=table_name,
                GlobalSecondaryIndexUpdates=[
                    {
                        'Create': {
                            'IndexName': index_name,
                            'KeySchema': [
                                {
                                    'AttributeName': pk_name,
                                    'KeyType': 'HASH'
                                }, {
                                    'AttributeName': sk_name,
                                    'KeyType': 'RANGE'
                                },
                            ],
                            'Projection': {
                                'ProjectionType': 'ALL',
                            },
                        },
                    }
                ]
            )
            print('UPDATE FDB TABLE INDEX...')
            return response
        except Exception as ex:
            print(ex)
            return True

    def delete_fdb_table(self):
        try:
            response = self.client.delete_table(
                TableName=self.table_name
            )
            return response
        except BaseException as ex:
            print(ex)
            return None

    def delete_item(self, pk, sk):
        response = self.get_table(self.table_name).delete_item(
            Key={
                '_pk': pk,
                '_sk': sk,
            },
            ReturnValues='ALL_OLD'
        )
        return response

    def get_table(self, table_name):
        # 캐싱된 테이블 객체 반환
        if table_name in self.table_cache:
            table = self.table_cache[table_name]
        else:
            table = self.resource.Table(table_name)
            self.table_cache[table_name] = table
        return table

    def get_item(self, pk, sk, consistent_read=True):
        table = self.get_table(self.table_name)
        key = {
            '_pk': pk,
            '_sk': sk
        }
        response = table.get_item(
            Key=key,
            ConsistentRead=consistent_read
        )
        item = response.get('Item', None)
        return item

    def put_item(self, item, can_overwrite=False):
        table = self.get_table(self.table_name)
        # 디비에 넣기전에 인덱스 타입을 고려하여 데이터를 변경한다.
        if can_overwrite:
            response = table.put_item(
                Item=item,
            )
            return response
        else:
            # 키가 이미 존재했을때 중복 쓰기를 방지하는 조건문 추가
            try:
                response = table.put_item(
                    Item=item,
                    ConditionExpression='attribute_not_exists(#pk) AND attribute_not_exists(#sk)',
                    ExpressionAttributeNames={
                        '#pk': '_pk',
                        '#sk': '_sk',
                    }
                )
                return response
            except self.resource.meta.client.exceptions.ConditionalCheckFailedException:
                pk = item['_pk']
                sk = item['_sk']
                raise Exception(f'Item already exist _pk:"{pk}" _sk:"{sk}"  Check "pk_field" and "sk_field" & "post_sk_fields" combination.')

    @classmethod
    def get_update_expression_attrs_pair(cls, item):
        """
        item 에서 업데이트 표현식과 속성을 튜플로 반환합니다.
        :param item:
        :return: (UpdateExpression, ExpressionAttributeValues)
        """
        expression = 'set'
        attr_names = {}
        attr_values = {}
        for idx, (key, value) in enumerate(item.items()):
            attr_key = '#key{}'.format(idx)
            attr_value = ':val{}'.format(idx)
            expression += ' {}={}'.format(attr_key, attr_value)

            attr_names['{}'.format(attr_key)] = key
            attr_values['{}'.format(attr_value)] = value
            if idx != len(item) - 1:
                expression += ','
        return expression, attr_names, attr_values

    def update_item(self, pk, sk, item):
        """
        아이탬을 업데이트합니다.
        만약 업데이트할 항목이 DB에 없는 경우 에러가 발생합니다.
        :param pk:
        :param sk:
        :param item:
        :return:
        """
        expression, attr_names, attr_values = self.get_update_expression_attrs_pair(item)
        attr_names['#pk'] = '_pk'
        attr_names['#sk'] = '_sk'
        try:
            response = self.get_table(self.table_name).update_item(
                Key={'_pk': pk, '_sk': sk},
                UpdateExpression=expression,
                ExpressionAttributeValues=attr_values,
                ExpressionAttributeNames=attr_names,
                ReturnValues="ALL_NEW",
                ConditionExpression='attribute_exists(#pk) AND attribute_exists(#sk)'
            )
        except Exception as ex:
            raise Exception('Item to update not exist')
        return response

    def batch_put(self, items, can_overwrite=False):
        table = self.get_table(self.table_name)
        if can_overwrite:
            # 중복 가능하면
            overwrite_by_keys = None
        else:
            # 불가능하면
            overwrite_by_keys = ['_pk', '_sk']
        with table.batch_writer(overwrite_by_pkeys=overwrite_by_keys) as batch:
            for item in items:
                batch.put_item(
                    Item=item,
                )
        return True

    def batch_delete(self, pk_sk_pairs):
        """
        :param pk_sk_pairs: [
            {
                'pk': '...',
                'sk': '...'
            }, ...
        ]
        :return:
        """
        table = self.get_table(self.table_name)
        with table.batch_writer() as batch:
            for pk_sk_pair in pk_sk_pairs:
                key = {
                    '_pk': pk_sk_pair['_pk'],
                    '_sk': pk_sk_pair['_sk']
                }
                batch.delete_item(Key=key)
        return True

    def _get_items(self, pk_sk_pairs, consistent_read=False, retry_attempt=0):
        keys = list([{
            '_pk': {'S': pk_sk_pair['_pk']},
            '_sk': {'S': pk_sk_pair['_sk']}
        } for pk_sk_pair in pk_sk_pairs if pk_sk_pair])
        if keys:
            response = self.client.batch_get_item(
                RequestItems={
                    self.table_name: {
                        'Keys': keys,
                        'ConsistentRead': consistent_read
                    }
                }
            )

            items_succeed = response['Responses'][self.table_name]

            # response 제대로 안왔을때 재시도 로직
            unprocessed_keys = response.get('UnprocessedKeys', {}).get(self.table_name, {}).get('Keys', [])
            if unprocessed_keys:
                # Backoff al.
                time.sleep(pow(retry_attempt + 1, 2))
                items_to_extend = self._get_items(unprocessed_keys, consistent_read, retry_attempt + 1)
                items_succeed.extend(items_to_extend)
        else:  # Keys 가 없을시 성공 내역 없음
            items_succeed = []

        for item in items_succeed:
            for key, value in item.items():
                value = type_deserializer.deserialize(value)
                item[key] = value

        return items_succeed

    def get_items(self, pk_sk_pairs, consistent_read=False):
        chunks = list(divide_chunks(pk_sk_pairs, 100))
        items_succeed = []
        futures = []
        # 배치 + 멀티스레드로 가져옵니다.
        with ThreadPoolExecutor(max_workers=max(1, len(chunks))) as worker:
            for chunk in chunks:
                futures.append(worker.submit(self._get_items, chunk, consistent_read))
        for future in futures:
            items_succeed.extend(future.result())

        # 요청한 순서대로 정렬합니다.
        items_by_key = {(item.get('_pk', ''), item.get('_sk', '')): item for item in items_succeed}
        sorted_items = []
        for pk_sk in pk_sk_pairs:
            if pk_sk:
                item = items_by_key.get((pk_sk['_pk'], pk_sk['_sk']), None)
                sorted_items.append(item)
            else:
                sorted_items.append(None)
        return sorted_items

    def query_items(self, partition_key_name, partition_key_value,
                    sort_condition, sort_key_name, sort_key_value, sort_key_second_value=None, filters=None,
                    start_key=None, reverse=False, limit=100, consistent_read=False, index_name=None,
                    recursive_filters=None):
        """
        AWS BOTO3 전용으로 쿼리 메서드 랩핑
        :param partition_key_name: 파티션키 속성의 이름
        :param partition_key_value: 파티션키 속성의 값
        :param sort_condition: 소트키 조건
        :param sort_key_name:
        :param sort_key_value:
        :param sort_key_second_value:
        :param filters: [
            {
                'field': '<FIELD>',
                'value': '<VALUE>',
                'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                        'is_in' | 'contains' | 'exist' | 'not_exist'
            }
        ]
        :param start_key:
        :param reverse:
        :param limit:
        :param consistent_read:
        :param index_name:
        :param recursive_filters: {  재귀 필터, or, and 연산을 묶어서 수행 가능합니다.
                'left': {
                    'field': '<FIELD>',
                    'value': '<VALUE>',
                    'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                            'is_in' | 'contains' | 'exist' | 'not_exist'
                },
                'operation': 'and',
                'right': {
                    'left': {
                        'field': '<FIELD>',
                        'value': '<VALUE>',
                        'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                                'is_in' | 'contains' | 'exist' | 'not_exist'
                    },
                    'operation': 'or',
                    'right': {
                        'field': '<FIELD>',
                        'value': '<VALUE>',
                        'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                                'is_in' | 'contains' | 'exist' | 'not_exist'
                    },
                },
            }
        :return:
        """
        # filters 타입 점검
        if filters and not isinstance(filters, list):
            raise Exception('filters should be list type')
        if recursive_filters and not isinstance(recursive_filters, dict):
            raise Exception('recursive_filters should be dict type')

        table = self.get_table(self.table_name)
        key_expression = Key(partition_key_name).eq(partition_key_value)
        if sort_condition == 'eq':
            key_expression &= Key(sort_key_name).eq(sort_key_value)
        elif sort_condition == 'lte':
            key_expression &= Key(sort_key_name).lte(sort_key_value)
        elif sort_condition == 'lt':
            key_expression &= Key(sort_key_name).lt(sort_key_value)
        elif sort_condition == 'gte':
            key_expression &= Key(sort_key_name).gte(sort_key_value)
        elif sort_condition == 'gt':
            key_expression &= Key(sort_key_name).gt(sort_key_value)
        elif sort_condition == 'btw':
            key_expression &= Key(sort_key_name).between(sort_key_value, sort_key_second_value)
        elif sort_condition == 'stw':
            key_expression &= Key(sort_key_name).begins_with(sort_key_value)
        elif sort_condition is None:
            pass
        else:
            raise Exception('sort_type must be one of [eq, lte, lt, gte, gt, btw, stw]')

        filter_expression = None
        if filters:
            for ft in filters:
                attr_to_add = self.get_attr(ft)
                if filter_expression:
                    filter_expression &= attr_to_add
                else:
                    filter_expression = attr_to_add
        elif recursive_filters:
            # 재귀 필터가 넘어온 경우, 딕셔너리 형태입니다.
            filter_expression = self.get_recursive_filters_expression(recursive_filters)

        args = {
            'Limit': limit,
            'ConsistentRead': consistent_read,
            'KeyConditionExpression': key_expression,
            'ScanIndexForward': not reverse,
        }
        if index_name:
            args['IndexName'] = index_name
            args['ConsistentRead'] = False  # index 사용시 일관된 읽기는 사용 불가
        if filter_expression:
            args['FilterExpression'] = filter_expression
        if start_key:
            args['ExclusiveStartKey'] = start_key
        # Decode to Decimal
        args = decode_dict(args)
        response = table.query(**args)
        return response

    @classmethod
    def get_recursive_filters_expression(cls, recursive_filters):
        # recursive_filters 로 부터, DynamoDB exp 를 구합니다.
        if not isinstance(recursive_filters, dict):
            raise Exception('<recursive_filters> must be type of <dict>')

        # dict 의 형식을 보고, 연산 결정
        if 'left' in recursive_filters and 'right' in recursive_filters and 'operation' in recursive_filters:
            filter_type = 'tuple'
        elif 'field' in recursive_filters and 'value' in recursive_filters and 'condition' in recursive_filters:
            filter_type = 'value'
        else:
            raise Exception('<recursive_filters> must consist of [<left> & <right> & <operation>] or '
                            '[<field> & <value> & <condition>]')

        # 실제 filter exp 변환
        filter_expression = None
        if filter_type == 'tuple':
            # left, right 타입 있는 경우, 재귀 진행.
            left = cls.get_recursive_filters_expression(recursive_filters['left'])
            right = cls.get_recursive_filters_expression(recursive_filters['right'])
            operation = recursive_filters['operation']
            if operation == 'and':
                filter_expression = left & right
            elif operation == 'or':
                filter_expression = left | right
            return filter_expression
        elif filter_type == 'value':
            # value 인 경우 바로 반환
            return cls.get_attr(recursive_filters)
        else:
            # 있을 수 없는 경우
            raise Exception('<filter_type> Error, must be one of <tuple> or <value>')

    @classmethod
    def get_attr(cls, ft):
        # filter 한개를 DynamoDB 의 ATTR 로 변환합니다.
        field = ft['field']
        value = ft.get('value', None)
        high_value = ft.get('second_value', None)
        cond = ft['condition']

        attr_to_add = Attr(field)
        if cond == 'eq':
            attr_to_add = attr_to_add.eq(value)
        elif cond == 'neq':
            attr_to_add = attr_to_add.ne(value)
        elif cond == 'lte':
            attr_to_add = attr_to_add.lte(value)
        elif cond == 'lt':
            attr_to_add = attr_to_add.lt(value)
        elif cond == 'gte':
            attr_to_add = attr_to_add.gte(value)
        elif cond == 'gt':
            attr_to_add = attr_to_add.gt(value)
        elif cond == 'btw':
            attr_to_add = attr_to_add.between(value, high_value)
        elif cond == 'not_btw':
            attr_to_add = ~attr_to_add.between(value, high_value)
        elif cond == 'stw':
            attr_to_add = attr_to_add.begins_with(value)
        elif cond == 'not_stw':
            attr_to_add = ~attr_to_add.begins_with(value)
        elif cond == 'is_in':
            attr_to_add = attr_to_add.is_in(value)
        elif cond == 'is_not_in':
            attr_to_add = ~attr_to_add.is_in(value)
        elif cond == 'contains':
            attr_to_add = attr_to_add.contains(value)
        elif cond == 'not_contains':
            attr_to_add = ~attr_to_add.contains(value)
        elif cond == 'exist':
            attr_to_add = attr_to_add.exists()
        elif cond == 'not_exist':
            attr_to_add = attr_to_add.not_exists()
        else:
            raise Exception('<condition> parameter must be one of '
                            '[eq, neq, lte, lt, gte, gt, btw, stw, is_in, contains, '
                            'not_btw, not_stw, not_is_in, not_contains, exist, not_exist]')
        return attr_to_add


class DynamoDB:
    def __init__(self, boto3_session, region='us-west-2', tag='SAWSI', endpoint_url=None):
        dynamo_config = botocore.client.Config(
            max_pool_connections=100,
            retries={
                'max_attempts': 10,  # 최대 재시도 횟수
                'mode': 'standard'  # 재시도 모드 (standard, adaptive)
            }
        )
        # endpoint_url 은 Local 서비스 사용시 활용됩니다.
        self.client = boto3_session.client('dynamodb', config=dynamo_config, region_name=region, endpoint_url=endpoint_url)
        self.resource = boto3_session.resource('dynamodb', config=dynamo_config, region_name=region, endpoint_url=endpoint_url)
        self.table_cache = {}
        self.cache = {}
        self.tag = tag

    def create_db_table(self, table_name:str, partition_key:str, partition_key_type:Literal["S", "N", "B"]='S',
                        sort_key:str=None, sort_key_type:Literal["S", "N", "B"]='S',
                        billing_mode='PAY_PER_REQUEST',
                        stream_enabled=False, stream_view_type='NEW_AND_OLD_IMAGES',
                        additional_attributes=None, additional_settings=None):
        """
        DynamoDB 테이블 생성 함수.
        :param table_name: 생성할 테이블의 이름.
        :param partition_key: 파티션 키의 이름.
        :param partition_key_type: 파티션 키의 타입 (기본값 'S'는 문자열).
        :param sort_key: 정렬 키의 이름 (선택 사항).
        :param sort_key_type: 정렬 키의 타입 (기본값 'S'는 문자열).
        :param billing_mode: 결제 모드 (기본값 'PAY_PER_REQUEST').
        :param stream_enabled: 스트림 활성화 여부 (기본값 False).
        :param stream_view_type: 스트림 뷰 타입 (기본값 'NEW_AND_OLD_IMAGES').
        :param additional_attributes: 추가적인 속성 정의 리스트 (선택 사항).
        :param additional_settings: create_table 호출에 사용될 추가 설정 사전 (선택 사항).

        :return: 생성된 테이블에 대한 응답.
        """
        attribute_definitions = [
            {
                'AttributeName': partition_key,
                'AttributeType': partition_key_type
            }
        ]
        key_schema = [
            {
                'AttributeName': partition_key,
                'KeyType': 'HASH'
            }
        ]
        if sort_key:
            attribute_definitions.append({
                'AttributeName': sort_key,
                'AttributeType': sort_key_type
            })
            key_schema.append({
                'AttributeName': sort_key,
                'KeyType': 'RANGE'
            })

        if additional_attributes:
            attribute_definitions.extend(additional_attributes)

        table_settings = {
            'AttributeDefinitions': attribute_definitions,
            'TableName': table_name,
            'KeySchema': key_schema,
            'BillingMode': billing_mode,
        }

        if stream_enabled:
            table_settings['StreamSpecification'] = {
                'StreamEnabled': True,
                'StreamViewType': stream_view_type
            }

        if additional_settings:
            table_settings.update(additional_settings)

        try:
            response = self.client.create_table(**table_settings)
            print(f'CREATING DB TABLE: [{table_name}] ...')
            self.client.get_waiter('table_exists').wait(TableName=table_name)
            return response
        except Exception as ex:
            print(ex)
            return False

    def enable_ttl(self, table_name: str, ttl_attribute_name: str):
        """
        DynamoDB 테이블에 대한 TTL 설정 활성화 함수.
        :param table_name: TTL을 활성화할 테이블의 이름.
        :param ttl_attribute_name: TTL 시간값을 담을 속성의 이름.
        :return: TTL 설정에 대한 응답.
        """
        try:
            response = self.client.update_time_to_live(
                TableName=table_name,
                TimeToLiveSpecification={
                    'Enabled': True,
                    'AttributeName': ttl_attribute_name
                }
            )
            print(f'TTL ENABLED FOR TABLE: [{table_name}] WITH ATTRIBUTE: [{ttl_attribute_name}]')
            return response
        except Exception as ex:
            print(ex)
            return False

    def create_gsi(
        self,
        table_name: str, index_name:str,
        partition_key: str, partition_key_type: str,
        sort_key: Optional[str] = None, sort_key_type: Optional[str] = None,
        projection_type: str = "ALL",
        read_capacity_units: Optional[int] = None, write_capacity_units: Optional[int] = None,
        additional_attributes: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        DynamoDB 테이블에 Global Secondary Index (GSI) 생성 함수.
        :param table_name: GSI를 추가할 DynamoDB 테이블의 이름.
        :param index_name: 인덱스 이름
        :param partition_key: GSI의 파티션 키 이름.
        :param partition_key_type: GSI의 파티션 키 데이터 타입 ('S', 'N', 'B').
        :param sort_key: GSI의 정렬 키 이름 (선택 사항).
        :param sort_key_type: GSI의 정렬 키 데이터 타입 ('S', 'N', 'B', 선택 사항).
        :param projection_type: GSI에 포함될 속성의 유형 ('ALL', 'KEYS_ONLY', 'INCLUDE').
        :param read_capacity_units: GSI의 읽기 용량 단위 (선택 사항, 프로비저닝 용량 모드일 경우).
        :param write_capacity_units: GSI의 쓰기 용량 단위 (선택 사항, 프로비저닝 용량 모드일 경우).
        :param additional_attributes: 추가 속성 정의 (선택 사항).
        :return: create_global_secondary_index 작업에 대한 응답.
        """
        # Example usage:
        # dynamodb = boto3.client('dynamodb', region_name='your-region')
        # manager = DynamoDBManager(dynamodb)
        # response = manager.create_gsi(
        #     table_name="YourTableName",
        #     index_name="YourIndexName",
        #     partition_key="YourPartitionKey",
        #     partition_key_type="S",
        #     sort_key="YourSortKey",
        #     sort_key_type="S",
        #     projection_type="ALL"
        # )

        attribute_definitions = [
            {
                'AttributeName': partition_key,
                'AttributeType': partition_key_type
            }
        ]

        if sort_key and sort_key_type:
            attribute_definitions.append({
                'AttributeName': sort_key,
                'AttributeType': sort_key_type
            })

        if additional_attributes:
            attribute_definitions.extend(additional_attributes)

        key_schema = [
            {
                'AttributeName': partition_key,
                'KeyType': 'HASH'
            }
        ]

        if sort_key:
            key_schema.append({
                'AttributeName': sort_key,
                'KeyType': 'RANGE'
            })
        # 인덱스 이름은 규칙에 따라 자동으로 할당함
        gsi = {
            'IndexName': index_name,
            'KeySchema': key_schema,
            'Projection': {
                'ProjectionType': projection_type
            },
        }

        if read_capacity_units and write_capacity_units:
            gsi['ProvisionedThroughput'] = {
                'ReadCapacityUnits': read_capacity_units,
                'WriteCapacityUnits': write_capacity_units
            }

        try:
            # 모든 인덱스가 생성되기 전까지 기다림
            self.wait_for_table_index_active(table_name)
            # 실제 생성
            response = self.client.update_table(
                TableName=table_name,
                AttributeDefinitions=attribute_definitions,
                GlobalSecondaryIndexUpdates=[
                    {
                        'Create': gsi
                    }
                ]
            )
            self.wait_for_table_active(table_name)
            print(f"GSI '{index_name}' has been requested for creation on table '{table_name}'.")
            return response
        except self.client.exceptions.ResourceNotFoundException:
            print(f"Table '{table_name}' not found.")
        except self.client.exceptions.ResourceInUseException:
            print(f"GSI '{index_name}' already exists or is being created or deleted.")
        except Exception as e:
            print(f"Failed to create GSI '{index_name}' on table '{table_name}': {e}")

        return {}

    def wait_for_table_active(self, table_name):
        """
        테이블이 ACTIVE 상태가 될 때까지 대기
        """
        print(f"Waiting for table '{table_name}' to become ACTIVE...")
        waiter = self.client.get_waiter('table_exists')
        try:
            waiter.wait(TableName=table_name, WaiterConfig={'Delay': 5, 'MaxAttempts': 20})
            print(f"Table '{table_name}' is now ACTIVE.")
        except ClientError as e:
            print(f"Error waiting for table '{table_name}' to become ACTIVE: {e}")

    def wait_for_table_index_active(self, table_name):
        """
        테이블 인덱스가 ACTIVE 상태가 될 때까지 대기
        """
        while True:
            print(f'Wait for table index status == active ..., table_name:{table_name}')
            # 테이블 상태를 가져옴
            response = self.client.describe_table(TableName=table_name)
            # 모든 글로벌 세컨더리 인덱스를 체크
            index_statuses = [index['IndexStatus'] for index in response['Table'].get('GlobalSecondaryIndexes', [])]

            # 모든 인덱스가 ACTIVE 상태인지 확인
            if all(status == 'ACTIVE' for status in index_statuses):
                break  # 모든 인덱스가 ACTIVE 상태이면 while 루프 종료
            time.sleep(10)  # 상태 확인 사이에 대기 시간을 추가

    def put_item(self, table_name: str, item: Dict[str, Any], can_overwrite:bool) -> Dict[str, Any]:
        """
        DynamoDB 테이블에 아이템을 저장하는 함수.

        :param table_name: 아이템을 저장할 테이블의 이름.
        :param item: 저장할 아이템, Python 사전 형식으로 DynamoDB 데이터 타입 규칙에 맞게 포맷됨.
        :param can_overwrite: 중복 저장 가능 여부 id 기준으로 판단
        :return: put_item 작업에 대한 응답.
        """
        table = self.get_table(table_name)
        if can_overwrite:
            response = table.put_item(
                Item=item,
            )
            return response
        else:
            # 키가 이미 존재했을때 중복 쓰기를 방지하는 조건문 추가
            try:
                response = table.put_item(
                    Item=item,
                    ConditionExpression='attribute_not_exists(#id)',
                    ExpressionAttributeNames={
                        '#id': 'id',
                    }
                )
                return response
            except self.resource.meta.client.exceptions.ConditionalCheckFailedException:
                _id = item['id']
                raise Exception(f'Item already exist id:"{_id}"')

    def delete_db_table(self, table_name):
        try:
            response = self.client.delete_table(
                TableName=table_name
            )
            return response
        except BaseException as ex:
            print(ex)
            return None


    def delete_item(self, table_name: str, key: Dict) -> None:
        """
        DynamoDB 테이블에서 아이템을 삭제하는 단순화된 인터페이스.
        :param table_name: 아이템을 삭제할 테이블의 이름.
        :param key: 삭제할 키
        """
        return self.get_table(table_name).delete_item(
            TableName=table_name,
            Key=key
        )

    def get_item(self, table_name: str, key: Dict, consistent_read:bool, use_cache=False) -> Dict[str, Any]:
        """
        DynamoDB 테이블에서 아이템을 조회하는 인터페이스.
        """
        # 캐시 사용 우선 검토
        c_key = f'{table_name}:{key}'
        if use_cache and c_key in self.cache:
            return self.cache[c_key]

        table = self.get_table(table_name)
        try:
            response = table.get_item(
                Key=key,
                ConsistentRead=consistent_read
            )
            item = response.get('Item', {})
            if item:
                # Save cache
                if len(self.cache) >= 100000:
                    self.cache = dict()
                self.cache[c_key] = item
            return item
        except Exception as e:
            print(f"Failed to retrieve item from table '{table_name}': {e}")
            return {}

    def get_table(self, table_name):
        # 캐싱된 테이블 객체 반환
        if table_name in self.table_cache:
            table = self.table_cache[table_name]
        else:
            table = self.resource.Table(table_name)
            self.table_cache[table_name] = table
        return table


    @classmethod
    def get_update_expression_attrs_pair(cls, item):
        """
        item 에서 업데이트 표현식과 속성을 튜플로 반환합니다.
        :param item:
        :return: (UpdateExpression, ExpressionAttributeValues)
        """
        expression = 'set'
        attr_names = {}
        attr_values = {}
        for idx, (key, value) in enumerate(item.items()):
            attr_key = '#key{}'.format(idx)
            attr_value = ':val{}'.format(idx)
            expression += ' {}={}'.format(attr_key, attr_value)

            attr_names['{}'.format(attr_key)] = key
            attr_values['{}'.format(attr_value)] = value
            if idx != len(item) - 1:
                expression += ','
        return expression, attr_names, attr_values


    def update_item(self, table_name:str, key:Dict, new_item:Dict):
        """
        아이탬을 업데이트합니다.
        만약 업데이트할 항목이 DB에 없는 경우 에러가 발생합니다.
        :return:
        """
        expression, attr_names, attr_values = self.get_update_expression_attrs_pair(new_item)
        for idx, k in enumerate(key.keys()):
            attr_names[f'#psk{idx}'] = k
        cond_exp = ' AND '.join(f'attribute_exists(#psk{idx})' for idx, _ in enumerate(key.keys()))
        try:
            response = self.get_table(table_name).update_item(
                Key=key,
                UpdateExpression=expression,
                ExpressionAttributeValues=attr_values,
                ExpressionAttributeNames=attr_names,
                ReturnValues="ALL_NEW",
                ConditionExpression=cond_exp
            )
        except Exception as ex:
            raise Exception(f'Item to update error: {ex}')
        return response


    def query_items(self, table_name:str, partition_key_name:str, partition_key_value:Any,
                    sort_condition:Optional[str], sort_key_name:str, sort_key_value:Any,
                    sort_key_second_value:Any=None, filters:List[Dict[Literal["field", "condition", "value"], Any]]=None,
                    start_key:Dict=None, reverse:bool=False, limit:int=100, consistent_read:bool=False,
                    index_name:str=None, recursive_filters:Dict=None):
        """
        AWS BOTO3 전용으로 쿼리 메서드 랩핑
        :param table_name: 테이블 이름
        :param partition_key_name: 파티션키 속성의 이름
        :param partition_key_value: 파티션키 속성의 값
        :param sort_condition: 소트키 조건
        :param sort_key_name:
        :param sort_key_value:
        :param sort_key_second_value:
        :param filters: [
            {
                'field': '<FIELD>',
                'value': '<VALUE>',
                'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                        'is_in' | 'contains' | 'exist' | 'not_exist'
            }
        ]
        :param start_key:
        :param reverse:
        :param limit:
        :param consistent_read:
        :param index_name:
        :param recursive_filters: {  재귀 필터, or, and 연산을 묶어서 수행 가능합니다.
                'left': {
                    'field': '<FIELD>',
                    'value': '<VALUE>',
                    'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                            'is_in' | 'contains' | 'exist' | 'not_exist'
                },
                'operation': 'and',
                'right': {
                    'left': {
                        'field': '<FIELD>',
                        'value': '<VALUE>',
                        'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                                'is_in' | 'contains' | 'exist' | 'not_exist'
                    },
                    'operation': 'or',
                    'right': {
                        'field': '<FIELD>',
                        'value': '<VALUE>',
                        'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                                'is_in' | 'contains' | 'exist' | 'not_exist'
                    },
                },
            }
        :return:
        """
        # filters 타입 점검
        if filters and not isinstance(filters, list):
            raise Exception('filters should be list type')
        if recursive_filters and not isinstance(recursive_filters, dict):
            raise Exception('recursive_filters should be dict type')

        # Decimal 필요할 경우
        partition_key_value = convert_if_number_to_decimal(partition_key_value)
        sort_key_value = convert_if_number_to_decimal(sort_key_value)
        sort_key_second_value = convert_if_number_to_decimal(sort_key_second_value)

        table = self.get_table(table_name)
        key_expression = Key(partition_key_name).eq(partition_key_value)
        if sort_condition == 'eq':
            key_expression &= Key(sort_key_name).eq(sort_key_value)
        elif sort_condition == 'lte':
            key_expression &= Key(sort_key_name).lte(sort_key_value)
        elif sort_condition == 'lt':
            key_expression &= Key(sort_key_name).lt(sort_key_value)
        elif sort_condition == 'gte':
            key_expression &= Key(sort_key_name).gte(sort_key_value)
        elif sort_condition == 'gt':
            key_expression &= Key(sort_key_name).gt(sort_key_value)
        elif sort_condition == 'btw':
            key_expression &= Key(sort_key_name).between(sort_key_value, sort_key_second_value)
        elif sort_condition == 'stw':
            key_expression &= Key(sort_key_name).begins_with(sort_key_value)
        elif sort_condition is None:
            pass
        else:
            raise Exception('sort_type must be one of [eq, lte, lt, gte, gt, btw, stw]')

        filter_expression = None
        if filters:
            for ft in filters:
                attr_to_add = self.get_attr(ft)
                if filter_expression:
                    filter_expression &= attr_to_add
                else:
                    filter_expression = attr_to_add
        elif recursive_filters:
            # 재귀 필터가 넘어온 경우, 딕셔너리 형태입니다.
            filter_expression = self.get_recursive_filters_expression(recursive_filters)

        args = {
            'Limit': limit,
            'ConsistentRead': consistent_read,
            'KeyConditionExpression': key_expression,
            'ScanIndexForward': not reverse,
        }
        if index_name:
            args['IndexName'] = index_name
            args['ConsistentRead'] = False  # index 사용시 일관된 읽기는 사용 불가
        if filter_expression:
            args['FilterExpression'] = filter_expression
        if start_key:
            args['ExclusiveStartKey'] = start_key

        args = decode_dict(args)
        response = table.query(**args)
        return response

    @classmethod
    def get_recursive_filters_expression(cls, recursive_filters):
        # recursive_filters 로 부터, DynamoDB exp 를 구합니다.
        if not isinstance(recursive_filters, dict):
            raise Exception('<recursive_filters> must be type of <dict>')

        # dict 의 형식을 보고, 연산 결정
        if 'left' in recursive_filters and 'right' in recursive_filters and 'operation' in recursive_filters:
            filter_type = 'tuple'
        elif 'field' in recursive_filters and 'value' in recursive_filters and 'condition' in recursive_filters:
            filter_type = 'value'
        else:
            raise Exception('<recursive_filters> must consist of [<left> & <right> & <operation>] or '
                            '[<field> & <value> & <condition>]')

        # 실제 filter exp 변환
        filter_expression = None
        if filter_type == 'tuple':
            # left, right 타입 있는 경우, 재귀 진행.
            left = cls.get_recursive_filters_expression(recursive_filters['left'])
            right = cls.get_recursive_filters_expression(recursive_filters['right'])
            operation = recursive_filters['operation']
            if operation == 'and':
                filter_expression = left & right
            elif operation == 'or':
                filter_expression = left | right
            return filter_expression
        elif filter_type == 'value':
            # value 인 경우 바로 반환
            return cls.get_attr(recursive_filters)
        else:
            # 있을 수 없는 경우
            raise Exception('<filter_type> Error, must be one of <tuple> or <value>')

    @classmethod
    def get_attr(cls, ft):
        # filter 한개를 DynamoDB 의 ATTR 로 변환합니다.
        field = ft['field']
        value = ft.get('value', None)
        value = convert_if_number_to_decimal(value)
        high_value = ft.get('second_value', None)
        high_value = convert_if_number_to_decimal(high_value)
        cond = ft['condition']

        attr_to_add = Attr(field)
        if cond == 'eq':
            attr_to_add = attr_to_add.eq(value)
        elif cond == 'neq':
            attr_to_add = attr_to_add.ne(value)
        elif cond == 'lte':
            attr_to_add = attr_to_add.lte(value)
        elif cond == 'lt':
            attr_to_add = attr_to_add.lt(value)
        elif cond == 'gte':
            attr_to_add = attr_to_add.gte(value)
        elif cond == 'gt':
            attr_to_add = attr_to_add.gt(value)
        elif cond == 'btw':
            attr_to_add = attr_to_add.between(value, high_value)
        elif cond == 'not_btw':
            attr_to_add = ~attr_to_add.between(value, high_value)
        elif cond == 'stw':
            attr_to_add = attr_to_add.begins_with(value)
        elif cond == 'not_stw':
            attr_to_add = ~attr_to_add.begins_with(value)
        elif cond == 'is_in':
            attr_to_add = attr_to_add.is_in(value)
        elif cond == 'is_not_in':
            attr_to_add = ~attr_to_add.is_in(value)
        elif cond == 'contains':
            attr_to_add = attr_to_add.contains(value)
        elif cond == 'not_contains':
            attr_to_add = ~attr_to_add.contains(value)
        elif cond == 'exist':
            attr_to_add = attr_to_add.exists()
        elif cond == 'not_exist':
            attr_to_add = attr_to_add.not_exists()
        else:
            raise Exception('<condition> parameter must be one of '
                            '[eq, neq, lte, lt, gte, gt, btw, stw, is_in, contains, '
                            'not_btw, not_stw, not_is_in, not_contains, exist, not_exist]')
        return attr_to_add

    def scan_dynamodb_table(self, table_name, filters:List[Dict[Literal["field", "condition", "value"], Any]]=None, recursive_filters: dict = None, start_key=None, limit=None):
        table = self.get_table(table_name)
        scan_kwargs = {}
        if limit:
            scan_kwargs['Limit'] = limit
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key

        filter_expression = None
        if filters:
            for ft in filters:
                attr_to_add = self.get_attr(ft)
                if filter_expression:
                    filter_expression &= attr_to_add
                else:
                    filter_expression = attr_to_add
        elif recursive_filters:
            # 재귀 필터가 넘어온 경우, 딕셔너리 형태입니다.
            filter_expression = self.get_recursive_filters_expression(recursive_filters)

        if filter_expression:
            scan_kwargs['FilterExpression'] = filter_expression

        response = table.scan(**scan_kwargs)
        return response

    def get_table_meta_info(self, table_name):
        # Table meta info
        table = self.get_table(table_name)
        table.load()

        return {
            'item_count': table.item_count,
            'table_name': table.table_name,
            'creation_date_time': table.creation_date_time,
            'table_status': table.table_status,
            'key_schema': table.key_schema,
            'table_size_bytes': table.table_size_bytes,
        }

    def get_table_names(self, last_evaluated_table: Optional[str] = None):
        if last_evaluated_table:
            response = self.client.list_tables(ExclusiveStartTableName=last_evaluated_table)
        else:
            response = self.client.list_tables()
        return response

    def get_stream_arn(self, table_name: str):
        # STREAM 이름 가져오기
        table_info = self.client.describe_table(TableName=table_name)
        stream_arn = table_info['Table']['LatestStreamArn']
        return stream_arn

    def set_stream_enabled(self, table_name: str, stream_enabled: bool, stream_view_type: str = 'NEW_AND_OLD_IMAGES'):
        """
        스트림 활성화
        """
        response = self.client.update_table(
            TableName=table_name,
            StreamSpecification={
                'StreamEnabled': stream_enabled,
                'StreamViewType': stream_view_type  # 필요한 데이터 유형 선택
            }
        )
        return response

    def get_stream_enabled(self, table_name: str) -> bool:
        """
        스트림 활성 여부 반환
        """
        table_info = self.client.describe_table(TableName=table_name)
        # 스트림 활성화 상태 확인
        stream_spec = table_info['Table'].get('StreamSpecification', None)

        if stream_spec and stream_spec.get('StreamEnabled', False):
            return True
        else:
            return False