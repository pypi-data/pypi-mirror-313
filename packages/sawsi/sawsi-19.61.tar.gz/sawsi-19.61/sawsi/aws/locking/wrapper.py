import time
import botocore
import botocore.client
from boto3.dynamodb.conditions import Key, Attr
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from concurrent.futures import ThreadPoolExecutor

type_deserializer = TypeDeserializer()
type_serializer = TypeSerializer()


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
                raise Exception(f'Item already exist. Check "pk_field" and "sk_field" & "post_sk_fields" combination.')

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
        with ThreadPoolExecutor(max_workers=len(chunks)) as worker:
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
