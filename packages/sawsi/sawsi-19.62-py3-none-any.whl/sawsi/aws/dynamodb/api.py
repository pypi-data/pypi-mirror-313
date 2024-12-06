"""
DynamoDB 를 사용하기 위한 인터페이스
"""
import json
import time
from sawsi.aws.dynamodb import util
from sawsi.aws.dynamodb import config, wrapper
from sawsi.aws import shared
from decimal import Decimal
from numbers import Number
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional, List, Literal, Any, Tuple


def encode_dict(dict_obj):
    def cast_number(v):
        if isinstance(v, dict):
            return encode_dict(v)
        if isinstance(v, list):
            return encode_dict(v)
        if isinstance(v, bool):
            return bool(v)
        if not isinstance(v, Number):
            return v
        if v % 1 == 0:
            return int(v)
        else:
            return float(v)

    if isinstance(dict_obj, dict):
        return {k: cast_number(v) for k, v in dict_obj.items()}
    elif isinstance(dict_obj, list):
        return [cast_number(v) for v in dict_obj]
    else:
        return dict_obj


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


def _find_proper_index_name(partition_object, pk_field, sk_field=None):
    """
    적절한 index 를 찾아 반환합니다.
    sk_field 가 None 인 경우에는 pk_field 가 일치하는 가장 빠른 인덱스를 반환합니다.
    sk_field 가 존재하는 경우 엄격하게 탐색해야합니다.
    :param partition_object:
    :param pk_field:
    :param sk_field:
    :return:
    """
    index_name = None
    pk_name = '_pk'
    sk_name = '_sk'
    if sk_field:
        # 엄격하게 탐색
        # 메인 파티션 먼저 검색
        if pk_field == partition_object['_pk_field'] and sk_field == partition_object['_sk_field']:
            index_name = None
        else:
            indexes = partition_object.get('indexes', [])
            for index in indexes:
                if pk_field == index['_pk_field'] and sk_field == index['_sk_field']:
                    # 완벽히 일치하면
                    index_name = index['index_name']
                    pk_name = index['pk_name']
                    sk_name = index['sk_name']
                    break
            if not index_name:
                # 인덱스가 안나올 경우, 매치되는게 없는 경우라..
                message = f'pk_field & sk_field pair must be one of \n'
                message += f"0. pk: <{partition_object['_pk_field']}> & sk: <{partition_object['_sk_field']}>\n"
                field_pairs = [f"{idx + 1}. pk: <{index['_pk_field']}> & sk: <{index['_sk_field']}>" for idx, index in enumerate(indexes)]
                message += '\n'.join(field_pairs)
                raise Exception(message)

    else:  # sk_field 없어도 pk_field 가 일치하면 우선 반환
        if pk_field == partition_object['_pk_field']:
            # 파티션에 있는 것과 일치할 경우
            index_name = None
        else:
            indexes = partition_object.get('indexes', [])
            for index in indexes:
                if pk_field == index['_pk_field']:
                    # 완벽히 일치하면
                    index_name = index['index_name']
                    pk_name = index['pk_name']
                    sk_name = index['sk_name']
                    break
            # 파티션에도 없고, 인덱스에도 없기 때문에 에러 레이즈
            if not index_name:
                message = f'pk_field & sk_field pair must be one of \n'
                message += f"0. pk: <{partition_object['_pk_field']}> & sk: <{partition_object['_sk_field']}>\n"
                field_pairs = [f"{idx + 1}. pk: <{index['_pk_field']}> & sk: <{index['_sk_field']}>" for idx, index in
                               enumerate(indexes)]
                message += '\n'.join(field_pairs)
                raise Exception(message)

    return index_name, pk_name, sk_name


def pop_ban_keys(item):
    """
    item 에서 _pk, _sk 등 시스템에서 보여줄 필요가 없는 것들을 pop
    :param item:
    :return:
    """
    if not item or not isinstance(item, dict):
        return item
    ban_keys = ['_pk', '_sk']
    for idx in range(1, 6):  # 최대 글로벌 인덱스 선언 개수가 5개
        ban_keys.append(f'_pk{idx}')
        ban_keys.append(f'_sk{idx}')
    item = item.copy()
    for ban_key in ban_keys:
        if ban_key in item:
            item.pop(ban_key)
    return item


def _fdb_format_value(k_value):
    """
    DB에서 연산하기 용이한 형태로, value 를 자리수 맞춤하여 반환.
    자리수를 맞춥니다. 숫자는 오른쪽부터 채우고 문자는 왼쪽부터 채웁니다.
        sk_digit_fit: 1234 인데 sk_digit_fit=8 이면, '____1234' 처럼 sorting 을 위해 자리를 채웁니다.
        소숫점이 들어오면 '____1234.43' 이런식으로 . 이하는 무시합니다.
        0이면 그대로 둡니다.
        문자열과 숫자 정렬 차이를 주기 위해 첫번째 문자로 차이를 만든다.
    :param value:
    :return:
    """
    sk_digit_fit = int(config.SK_DIGIT_FIT)
    if isinstance(k_value, (int, float, Decimal)):
        sk_value = util.convert_int_to_custom_base64(util.unsigned_number(k_value))
        sk_value = 'D' + sk_value.rjust(sk_digit_fit)
    else:
        # 삽입시에는 무조건 자릿수 맞춤을 하지만, 쿼리시에는 eq 일때만 자릿수 맞춤을 해준다.
        sk_value = str(k_value)
        sk_value = 'S' + sk_value + config.END_NOTATION  # 자리수 맞춤 대신에, 종료 제어 문자를 삽입하여 표기함.
    return sk_value


class DynamoFDBAPI:
    """
    DynamoDB 를 One Table 형태로 만들어 활용하는 커스텀 ORM 클래스
    """
    def __init__(self, table_name, credentials=None, region=shared.DEFAULT_REGION):
        """
        :param table_name: "테이블 이름"
        :param credentials: {
            "aws_access_key_id": "str",
            "aws_secret_access_key": "str",
            "region_name": "str",
            "profile_name": "str"
        }
        """
        self.boto3_session = shared.get_boto_session(credentials)
        self.cache = {}
        self.table_name = table_name
        self.dynamoFDB = wrapper.DynamoFDB(self.boto3_session, table_name, region)

    def init_table(self):
        # 테이블을 초기화합니다.
        self.dynamoFDB.init_fdb_table()

    # 새로 추가된 FastDatabase, Fully NoSQL
    @classmethod
    def _fdb_item_id_to_pk_sk_pair(cls, item_id):
        """
        내부적으로 pk와 sk 조합을 item_id 로 부터 복호화합니다.
        :param item_id:
        :return:
        """
        try:
            pk, sk = util.split_pk_sk(item_id)
            return {
                '_pk': pk,
                '_sk': sk
            }
        except:
            return None

    @classmethod
    def _fdb_pk_sk_to_item_id(cls, pk, sk):
        """
        pk 와 sk 를 item_id 로 암호화합니다.
        :param pk:
        :param sk:
        :return:
        """
        return util.merge_pk_sk(pk, sk)

    def fdb_create_partition(self, partition, pk_field, sk_field=None, uk_fields=None, create_default_index=True):
        """
        Fast DB 내부에 파티션을 생성합니다. 사실 생성의 개념보다는 파티션을 선언합니다.
        파티션이 이미 있으면, 업데이트합니다.
        파티션 삭제시에, 내부 데이터는 삭제 되지 않기 때문에 유의해야합니다.
        :param partition: order 등 파티션 이름
        :param pk_field: user_id 등을 pk_field 로 지정하는것이 유리합니다. 병렬 처리와 관련 있으며, 디버깅을 위해
        실제 DB의 pk 필드 (인덱스) 에는 <pk_field>#<pk.value> 의 값이 들어갑니다.
        :param sk_field: created_at 등.. 날짜로 구성하면 날짜별 정렬이 가능합니다.
        :param uk_fields: 소트키 뒤에 붙는 field 입니다. 임의로 데이터 중복 생성 방지 기능을 만드는데 유용합니다.
        :param can_overwrite:
        :param create_default_index: 기본 인덱스로, _ptn, _crt 를 생성합니다.
        :return:
        """
        self._fdb_remove_partition_cache()
        response = self.dynamoFDB.put_item({
            '_pk': config.STR_META_INFO_PARTITION,
            '_sk': partition,
            '_partition_name': partition,
            '_pk_field': pk_field,
            '_sk_field': sk_field,
            '_uk_fields': uk_fields,
            '_crt': int(time.time()),
        }, can_overwrite=False)
        result_item = response.get('Attributes', {})
        if create_default_index:
            self.fdb_append_index(partition, '_ptn', '_crt')
        return result_item

    def fdb_update_partition(self, partition, pk_field, sk_field=None, uk_fields=None):
        """
        Fast DB 내부에 파티션을 생성합니다. 사실 생성의 개념보다는 파티션을 선언합니다.
        파티션이 이미 있으면, 업데이트합니다.
        파티션 삭제시에, 내부 데이터는 삭제 되지 않기 때문에 유의해야합니다.
        :param partition: order 등 파티션 이름
        :param pk_field: user_id 등을 pk_field 로 지정하는것이 유리합니다. 병렬 처리와 관련 있으며, 디버깅을 위해
        실제 DB의 pk 필드 (인덱스) 에는 <pk_field>#<pk.value> 의 값이 들어갑니다.
        :param sk_field: created_at 등.. 날짜로 구성하면 날짜별 정렬이 가능합니다.
        :param uk_fields: 소트키 뒤에 붙는 field 입니다. 임의로 데이터 중복 생성 방지 기능을 만드는데 유용합니다.
        :param can_overwrite:
        :param create_default_index: 기본 인덱스로, _ptn, _crt 를 생성합니다.
        :return:
        """
        self._fdb_remove_partition_cache()
        response = self.dynamoFDB.update_item(config.STR_META_INFO_PARTITION, partition, {
            '_pk_field': pk_field,
            '_sk_field': sk_field,
            '_uk_fields': uk_fields,
            '_crt': int(time.time()),
        })
        result_item = response.get('Attributes', {})
        return result_item

    def fdb_append_index(self, partition_name, pk_field, sk_field):
        """
        DB partition 에 인덱스를 추가합니다.
        indexes 보고 순서에 따라 결정.
        :param partition_name:
        :param pk_field:
        :param sk_field:
        :return:
        """
        partitions = self.fdb_get_partitions()
        partitions = [p for p in partitions if p.get('_partition_name', '') == partition_name]
        if not partitions:
            raise Exception(f'No such partition: {partition_name}')
        partition = partitions[0]
        indexes = partition.get('indexes', [])
        # 사용가능한 최소 인덱스 넘버 찾기
        index_number = None
        for idx_num in range(1, 20):
            has_number = False
            for index in indexes:
                if index['index_number'] == idx_num:
                    has_number = True
            if not has_number:
                index_number = idx_num
                break
        if index_number is None:
            raise Exception('허용 가능한 인덱스 수량 초과')
        pk_name = f"_pk{index_number}"
        sk_name = f"_sk{index_number}"
        index_name = f'{pk_name}-{sk_name}'

        try:
            # 실제 FDB 에 인덱스가 없으면 생성 있으면 Pass
            self.dynamoFDB.create_fdb_partition_index(self.dynamoFDB.table_name, index_name, pk_name, sk_name)
        except Exception as ex:
            print(ex)
            pass

        for index in indexes:
            if index['_pk_field'] == pk_field and index['_sk_field'] == sk_field:
                raise Exception('<_pk_field> & <_sk_field>  already exist in index')
        index_item = {
            '_pk_field': pk_field,
            '_sk_field': sk_field,
            'pk_name': pk_name,
            'sk_name': sk_name,
            'index_number': index_number,
            'index_name': index_name
        }

        indexes.append(index_item)
        partition['indexes'] = indexes
        return self.dynamoFDB.update_item(config.STR_META_INFO_PARTITION, partition_name, {
            'indexes': indexes
        })

    def fdb_detach_index(self, partition_name, index_name):
        partitions = self.fdb_get_partitions()
        partitions = [p for p in partitions if p.get('_partition_name', '') == partition_name]
        if not partitions:
            raise Exception(f'No such partition: {partition_name}')
        partition = partitions[0]
        indexes = partition.get('indexes', [])
        # index_name 를 제거
        indexes = [index for index in indexes if index.get('index_name', '') != index_name]
        partition['indexes'] = indexes
        return self.dynamoFDB.update_item(config.STR_META_INFO_PARTITION, partition_name, partition)

    def fdb_remove_all_index(self, partition_name):
        # 위험한 함수, 인덱스 전체 제거
        partitions = self.fdb_get_partitions()
        partitions = [p for p in partitions if p.get('_partition_name', '') == partition_name]
        if not partitions:
            raise Exception(f'No such partition: {partition_name}')
        partition = partitions[0]

        # index 를 제거
        indexes = []
        partition['indexes'] = indexes
        return self.dynamoFDB.update_item(config.STR_META_INFO_PARTITION, partition_name, partition)

    def _fdb_remove_partition_cache(self):
        """
        캐시 삭제, 새로운 파티션 추가시 필요!
        :return:
        """
        if 'partitions' in self.cache:
            self.cache.pop('partitions')

    def fdb_get_partition(self, partition_name, use_cache=True):
        """
        실제 파티션을 반환
        :param partition_name:
        :param use_cache: 캐시 사용
        :return:
        """
        pts = self.fdb_get_partitions(use_cache=use_cache)
        for pt in pts:
            if pt['_partition_name'] == partition_name:
                return pt
        return False

    def fdb_get_partitions(self, use_cache=False):
        """
        파티션 목록을 가져옵니다.
        :return:
        """
        # 캐시 있으면 먼저 반환, 최대 100초간 유효
        cache_key = 'partitions' + str(int(time.time() // 100))
        if use_cache and cache_key in self.cache:
            return [it.copy() for it in self.cache[cache_key]]

        # 반복하면서 end_key 없을때까지 수행
        items = []
        start_key = None
        while True:
            response = self.dynamoFDB.query_items(
                '_pk', config.STR_META_INFO_PARTITION, 'gte', '_sk', ' ',
                limit=1000, consistent_read=True, start_key=start_key
            )
            _items = response.get('Items', [])
            start_key = response.get('LastEvaluatedKey', None)
            items.extend(_items)
            if not start_key:
                break

        # 필요 없는 키 제거
        for item in items:
            item.pop('_pk')
            item.pop('_sk')

        # 자주 콜 됨, 비용이 비싸기때문에 캐싱
        items = [encode_dict(item) for item in items]
        items = [it.copy() for it in items]
        self.cache[cache_key] = items
        return items

    def fdb_delete_partition(self, partition):
        """
        파티션을 삭제, 내부 데이터는 별도로 삭제해야합니다.
        :param partition:
        :return:
        """
        self._fdb_remove_partition_cache()
        response = self.dynamoFDB.delete_item(config.STR_META_INFO_PARTITION, partition)
        return response

    def fdb_has_pk_sk_by_item(self, partition, item, consistent_read=True):
        """
        item 의 pk-sk 조합이 이미 DB에 존재하는지 확인합니다.
        :param partition:
        :param item:
        :param consistent_read: 최신정보로 확인할건지
        :return:
        """
        item = self._fdb_process_item_with_partition(item, partition)
        item_id = item.get('_id', None)
        if item_id:
            item = self.fdb_get_item(item_id, consistent_read)
            if item:
                return True
        return False

    def _fdb_process_item_with_partition(self, item, partition, for_creation=True):
        """
        item 을 DB에 넣기 전에 partition 에서 정하는 형태와 동일하게 매핑합니다.
        :param item:
        :param partition:
        :param for_creation: update 시에는 False 로 해야 키 중첩이 안됨.
        :return:
        """
        partitions = self.fdb_get_partitions(use_cache=True)
        partitions_by_name = {
            p.get('_partition_name', None): p for p in partitions
        }
        partition_obj = partitions_by_name.get(partition, None)
        if not partition_obj:
            raise Exception(f'No such partition: {partition}')

        pk_field = partition_obj['_pk_field']
        sk_field = partition_obj['_sk_field']
        uk_fields = partition_obj.get('_uk_fields', [])

        # 인덱스 정보 받기.
        indexes = partition_obj.get('indexes', [])
        if for_creation:
            # 업데이트시에는 시간 변경하면 안됨
            item['_crt'] = int(time.time())
        item['_ptn'] = partition
        item = decode_dict(item)

        pk_value = ''
        # 생성할때만, pk sk 검사
        if for_creation:
            if pk_field not in item:
                raise Exception(f'pk_field:["{pk_field}"] should in item')
            if sk_field and sk_field not in item:
                raise Exception(f'sk_field:["{sk_field}"] should in item')
            pk_value = item[pk_field]

        # sk 관련 변수 생성
        if sk_field and sk_field in item:
            sk_value = item[sk_field]
        else:
            sk_value = ''

        # 자리수를 맞춥니다. 숫자는 오른쪽부터 채우고 문자는 왼쪽부터 채웁니다.
        sk_value = _fdb_format_value(sk_value)

        if sk_field is None:
            # None 이 그대로 삽입되는걸 방지
            sk_field = ''
        # pk = f'{pk_group}#{pk_field}#{pk_value}'
        # sk = f'{sk_group}#{partition}#{sk_field}#{sk_value}'
        if pk_field == '_ptn':
            # pk_field 가 파티션일 경우 중복되는 지점을 줄여서 표현해서 용량 아끼기
            pk = f'{partition}'
        else:
            pk = f'{partition}#{pk_field}#{pk_value}'
        sk = f'{sk_field}#{sk_value}'

        if uk_fields:
            for uk_field in uk_fields:
                uk_value = item.get(uk_field, '')
                # 자리수 맞춤 수행
                uk_value = _fdb_format_value(uk_value)
                sk += f'#{uk_field}#{uk_value}'

        item['_pk'] = pk
        item['_sk'] = sk

        # 인덱스에 넣을 것들 맵핑
        for index in indexes:
            pk_name = index['pk_name']  # _pk2 ... 같은것들
            sk_name = index['sk_name']  # _sk2 ... 같은것들
            pk_field = index['_pk_field']
            sk_field = index['_sk_field']
            has_pk = pk_field in item
            has_sk = sk_field in item

            pk_value = item.get(pk_field, None)

            if sk_field:
                sk_value = item.get(sk_field, '')
            else:
                sk_value = ''

            # 자리수를 맞춥니다. 숫자는 오른쪽부터 채우고 문자는 왼쪽부터 채웁니다.
            sk_value = _fdb_format_value(sk_value)

            if sk_field is None:
                # None 이 그대로 삽입되는걸 방지
                sk_field = ''

            # 인덱스용으로 생성되는 pk_n
            # _pk_v = f'{pk_group}#{pk_field}#{pk_value}'
            # _sk_v = f'{sk_group}#{partition}#{sk_field}#{sk_value}'
            if pk_field == '_ptn':
                # pk_field 가 파티션일 경우 중복되는 지점을 줄여서 표현해서 용량 아끼기
                _pk_v = f'{partition}'
            else:
                _pk_v = f'{partition}#{pk_field}#{pk_value}'
            _sk_v = f'{sk_field}#{sk_value}'

            if for_creation:
                # 생성용이면 무조건 인덱스 키 삽입
                item[pk_name] = _pk_v
                item[sk_name] = _sk_v
            else:
                # 업데이트 용일 경우 인덱스 키 삽입하면 안됨, 단 업데이트를 명시적으로 한 경우만 키 삽입
                if has_pk:
                    item[pk_name] = _pk_v
                if has_sk:
                    item[sk_name] = _sk_v

        item['_id'] = self._fdb_pk_sk_to_item_id(pk, sk)
        return item

    def fdb_put_items(self, partition, items, can_overwrite=False):
        """
        배치 생성.
        item 삽입 전에 파티션을 불러와서 매칭을 잘 확인해야합니다.
        :param partition:
        :param items:
        :param can_overwrite:
        :return:
        """
        futures = []
        def _put(_it):
            try:
                r = self.fdb_put_item(partition, _it, can_overwrite)
                return r
            except Exception as ex:
                print(ex)
                return None

        with ThreadPoolExecutor(max_workers=10) as executor:
            for item in items:
                future = executor.submit(_put, item)
                futures.append(future)
        results = [future.result() for future in futures]
        return results

    def fdb_put_item(self, partition, item, can_overwrite=False):
        """
        생성
        :param partition:
        :param item:
        :param can_overwrite: 덮어쓰기 가능한지
        :return:
        """
        item = self._fdb_process_item_with_partition(item, partition)
        _id = item.get('_id', None)
        # ID 는 _pk, _sk 와 1:1 대응 하기 때문에 저장하지 않습니다.
        if '_id' in item:
            item.pop('_id')
        response = self.dynamoFDB.put_item(item, can_overwrite)
        item['_id'] = _id
        item = pop_ban_keys(item)
        item = encode_dict(item)
        return item

    def fdb_get_items(self, item_ids, consistent_read=False):
        """
        item_ids 를 배치로 쿼리하여 가져옵니다.
        :param item_ids:
        :param consistent_read:
        :return:
        """
        items = self.dynamoFDB.get_items(
            [self._fdb_item_id_to_pk_sk_pair(item_id) for item_id in item_ids],
            consistent_read=consistent_read
        )
        for item in items:
            if item:
                item['_id'] = util.merge_pk_sk(item['_pk'], item['_sk'])
        # Decimal 등 값을 int, float 으로 캐스팅
        items = [encode_dict(item) for item in items]
        # 필요 없는 값 제거
        items = [pop_ban_keys(item) for item in items]
        return items

    def fdb_get_item(self, item_id, consistent_read=False):
        pair = self._fdb_item_id_to_pk_sk_pair(item_id)
        if not pair:
            raise Exception(f'Invalid item_id: "{item_id}"')
        _pk = pair['_pk']
        _sk = pair['_sk']
        item = self.dynamoFDB.get_item(_pk, _sk, consistent_read)
        if not item:
            # 없으면 그냥..
            return None
        # ID 생성해주고
        item['_id'] = util.merge_pk_sk(item['_pk'], item['_sk'])
        # Decimal 등 값을 int, float 으로 캐스팅
        item = encode_dict(item)
        # 필요 없는 값 제거
        item = pop_ban_keys(item)
        return item

    def fdb_get_item_by_key(self, pk, sk, consistent_read=False):
        item = self.dynamoFDB.get_item(pk, sk, consistent_read)
        if not item:
            # 없으면 그냥..
            return None
        # ID 생성해주고
        item['_id'] = util.merge_pk_sk(item['_pk'], item['_sk'])
        # Decimal 등 값을 int, float 으로 캐스팅
        item = encode_dict(item)
        # 필요 없는 값 제거
        item = pop_ban_keys(item)
        return item


    def _fdb_query_items_low(self, pk_field, pk_value, sort_condition=None,
                        partition='', sk_field='', sk_value=None, sk_second_value=None, filters=None,
                        start_key=None, limit=100, reverse=False, consistent_read=False, index_name=None,
                        pk_name='_pk', sk_name='_sk', recursive_filters=None):
        """
        DB 를 쿼리하고, 이는 NoSQL 최적화 되어 있습니다. (로우레벨)
        단계별로 pk 관련 키들은 쿼리에 필수이며,
        sk 관련 키들은 단계별로 아이템 쿼리를 진행할 수 있도록 도와줍니다.
        partition 을 넘겨야, sk_value 를 입력할 수 있기 때문에,
        sk_field 를 파티션을 통해 구할 수 있습니다.
        :param pk_field:
        :param pk_value:
        :param sort_condition:
        :param partition:
        :param sk_field:
        :param sk_value:
        :param sk_second_value:
        :param filters: [
            {
                'field': '<FIELD>',
                'value': '<VALUE>',
                'second_value': '<SECOND_VALUE>' | None, # btw 연산자 사용시 사용
                'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                        'is_in' | 'contains' | 'exist' | 'not_exist'
            }
        ]
        :param start_key:
        :param limit:
        :param reverse:
        :param consistent_read:
        :param index_name: 없을시 기본 파라메터로 쿼리
        :param pk_name:
        :param sk_name:
        :param recursive_filters: {
            'left': {
                'field': '<FIELD>',
                'value': '<VALUE>',
                'second_value': '<SECOND_VALUE>' | None, # btw 연산자 사용시 사용
                'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                        'is_in' | 'contains' | 'exist' | 'not_exist'
            },
            'operation': 'and' | 'or',
            'right': {
                'left': {
                    'field': '<FIELD>',
                    'value': '<VALUE>',
                    'second_value': '<SECOND_VALUE>' | None, # btw 연산자 사용시 사용
                    'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                            'is_in' | 'contains' | 'exist' | 'not_exist'
                },
                'operation': 'and' | 'or',
                'right': {...},
            },
        }
        :return:
        """
        if partition is not None:
            partitions = self.fdb_get_partitions(use_cache=True)
            partitions_by_name = {
                p.get('_partition_name', None): p for p in partitions
            }
            partition_obj = partitions_by_name.get(partition, None)
            if not partition_obj:
                raise Exception(f'No such partition: {partition}')

            # p_pk_field = partition_obj['_pk_field']
            #
            # if p_pk_field != pk_field:
            #     raise Exception(f'pk_field must be a [{p_pk_field}]')

        sk_digit_fit = int(config.SK_DIGIT_FIT)
        # 자리수를 맞춥니다. 숫자는 오른쪽부터 채우고 문자는 왼쪽부터 채웁니다.
        if sk_value is not None:
            if isinstance(sk_value, (int, float, Decimal)):
                sk_value = util.convert_int_to_custom_base64(util.unsigned_number(sk_value))
                sk_value = 'D' + sk_value.rjust(sk_digit_fit)
                if sort_condition == 'eq':
                    sort_condition = 'stw'
            else:
                sk_value = str(sk_value)
                if sort_condition == 'eq':
                    sk_value = sk_value + config.END_NOTATION  # 자리수 맞춤 대신 종료 제어 문자 표기
                    # 자리수를 맞췄기 때문에 stw 이 eq 와 동일한 효과를 낸다.
                    # eq 는 쓰면 뒤에 있는 것들 때문에 쿼리가 안됨.
                    sort_condition = 'stw'
                sk_value = 'S' + sk_value
        else:
            sk_value = ''

        if sk_second_value is not None:
            if isinstance(sk_second_value, (int, float, Decimal)):
                sk_second_value = util.convert_int_to_custom_base64(util.unsigned_number(sk_second_value))
                sk_second_value = 'D' + sk_second_value.rjust(sk_digit_fit)
            else:
                sk_second_value = str(sk_second_value)
                sk_second_value = 'S' + sk_second_value
        else:
            sk_second_value = ''

        if pk_field == '_ptn':
            # pk_field 가 파티션일 경우 중복되는 지점을 줄여서 표현해서 용량 아끼기
            pk = f'{partition}'
        else:
            pk = f'{partition}#{pk_field}#{pk_value}'

        if not sk_field:
            # sort key 의 맨 처음 부분이기 때문에 문자 하나는 있어야 함, 공백 문자 삽입
            sk_field = ' '

        sk = f'{sk_field}'
        # if partition:  삭제함 pk 그룹에 포함시킴
        #     sk += f'#{partition}'

        # sk_second_value 가 있을 경우 sk_high 비교 변수 생성
        sk_high = ''
        if sk_second_value:
            sk_high = sk + f'#{sk_second_value}'
        if sk_value:
            sk += f'#{sk_value}'
            # TODO LTE, GT 일때, 뒤에 postfix 가 있으면 경우에 따라 eq 조건이 재대로 적용되지 않는 문제 해결
            if sort_condition == 'gt':
                # GT 일때, POSTFIX 때문에, EQ 조건이 같이 걸리는걸 방지하고자 뒤에다가 가장 큰 수치를 붙임
                # row 내 sk_value 다음에는 # 이기 때문에 이것보다 크면 됨.
                sk += 'A'
            elif sort_condition == 'lte':
                # LTE 일때, POSTFIX 를 # 보다 큰것으로 변경
                sk += 'A'

        response = self.dynamoFDB.query_items(pk_name, pk,
                                              sort_condition, sk_name, sk,
                                              sort_key_second_value=sk_high, filters=filters,
                                              start_key=start_key, reverse=reverse, limit=limit,
                                              consistent_read=consistent_read, index_name=index_name,
                                              recursive_filters=recursive_filters)
        end_key = response.get('LastEvaluatedKey', None)
        items = response.get('Items', [])

        # ID 매겨줌
        for item in items:
            if item:
                # 여기서 pkn, skn 을 쓰지 않는 이유는... ID 용이기 때문이다.
                item['_id'] = util.merge_pk_sk(item['_pk'], item['_sk'])

        return items, end_key

    def fdb_delete_items(self, item_ids):
        """
        배치 삭제, 여러개를 한번에 삭제
        :param item_ids:
        :return:
        """
        self.dynamoFDB.batch_delete([self._fdb_item_id_to_pk_sk_pair(item_id) for item_id in item_ids])

    def fdb_delete_item(self, item_id):
        """
        아이템을 삭제하고, 삭제한 내용을 반환합니다.
        삭제한 내용이 없는 경우 없는 객체를 삭제 시도한 경우입니다.
        :param item_id:
        :return:
        """
        pair = self._fdb_item_id_to_pk_sk_pair(item_id)
        if not pair:
            raise Exception(f'Invalid item_id: "{item_id}"')
        _pk = pair['_pk']
        _sk = pair['_sk']
        response = self.dynamoFDB.delete_item(_pk, _sk)
        deleted_item = response.get('Attributes')
        deleted_item = encode_dict(deleted_item)
        return deleted_item

    def _fdb_check_sk_safe(self, partition, origin_sk, new_sk):
        """
        sk 가 업데이트했을시 소트키에 영향이 없는지 판단합니다.
        :param partition:
        :param origin_sk: 원래 sk
        :param new_sk:
        :return:
        """
        partitions = self.fdb_get_partitions(use_cache=True)
        partitions_by_name = {
            p.get('_partition_name', None): p for p in partitions
        }
        partition_obj = partitions_by_name.get(partition, None)
        if not partition_obj:
            raise Exception(f'No such partition: {partition}')
        return new_sk == origin_sk

    def _fdb_check_keys_cannot_update(self, partition_name):
        # 업데이트할 수 없는 키 목록 반환
        keys_cannot_update = set()
        pt = self.fdb_get_partition(partition_name, use_cache=True)
        if not pt:
            raise Exception(f'No such partition: {partition_name}')
        pk_field = pt['_pk_field']
        sk_field = pt['_sk_field']
        uk_fields = pt['_uk_fields']
        keys_cannot_update.add(pk_field)
        keys_cannot_update.add(sk_field)
        if uk_fields:
            for uk_field in uk_fields:
                keys_cannot_update.add(uk_field)
        return keys_cannot_update

    def fdb_update_item(self, partition_name, item_id, item):
        """
        1. pk 와 sk 는 업데이트할 수 없음. -> key 로 사용되는 필드가 포함되어 있는지 확인. 있으면 에러
        2. 실제 업데이트 수행. 혹시 모르니, key 로 사용되는 필드가 변경되는지 조건문 확인할것.
        :param partition_name:
        :param item_id:
        :param item:
        :return:
        """
        # 업데이트 전에 파티션을 확인
        old_item = self.fdb_get_item(item_id)
        if not old_item:
            raise Exception(f'No such item: {item_id}')
        if old_item['_ptn'] != partition_name:
            raise Exception(f'Partition not match: {partition_name} != {old_item["_ptn"]}')

        # Item ID 로부터, pk, sk 만들기
        pk_sk_pair = self._fdb_item_id_to_pk_sk_pair(item_id)
        origin_pk = pk_sk_pair['_pk']
        origin_sk = pk_sk_pair['_sk']

        # key 로 사용되는 필드가 포함되어 있는지 확인.
        key_fields = self._fdb_check_keys_cannot_update(partition_name)

        # 레퍼런스가 되는 상황 방지를 위해 copy 사용
        item_to_insert = item.copy()
        for key_field in key_fields:
            if key_field in item_to_insert:
                item_to_insert.pop(key_field)
                print(f'You cannot update key fields: {key_field}')

        # Index 도 같이 업데이트 해주기
        item_to_insert = self._fdb_process_item_with_partition(item_to_insert, partition_name, for_creation=False)
        # pk, sk 는 업데이트할 수 없음. 따라서 대상에서 제외, 어차피 위에서 걸림.
        ban_keys = ['_pk', '_sk', '_id', '_crt', '_ptn']
        for ban_key in ban_keys:
            if ban_key in item_to_insert:
                item_to_insert.pop(ban_key)

        # 실젱 업데이트 수행
        response = self.dynamoFDB.update_item(origin_pk, origin_sk, item_to_insert)
        attributes = response.get('Attributes', {})  # 업데이트 결과
        # 성공한 경우, _id 도 함께 반환해줌.
        if attributes:
            attributes['_id'] = item_id
        attributes = encode_dict(attributes)  # Python 내부에서 사용하기 적절한 변수형으로 캐스팅
        attributes = pop_ban_keys(attributes)
        return attributes

    def fdb_update_items(self, partition_name, item_pairs:Dict[str, Dict], max_workers=10):
        futures = []
        with ThreadPoolExecutor(max_workers=max_workers) as worker:
            for item_id, item in item_pairs.items():
                future = worker.submit(self.fdb_update_item, partition_name, item_id, item)
                futures.append(future)
        return [future.result() for future in futures]

    def fdb_generate_items(self, partition, pk_field=None, sk_field=None, pk_value=None,
                           sk_condition=None, sk_value=None, sk_second_value=None,
                           filters=None, recursive_filters=None, reverse=False, consistent_read=False,
                           limit=500, max_scan_rep=100):
        """
        query API 를 래핑하여 쓰기 편하게 items 로만 반환합니다.
        :param partition: 조회할 파티션
        :param pk_field:
        :param sk_field:
        :param pk_value:
        :param sk_condition:
        :param sk_value:
        :param sk_second_value:
        :param filters:
        :param recursive_filters:
        :param reverse:
        :param consistent_read:
        :param limit:
        :param max_scan_rep:
        :return:
        """
        start_key = None
        while True:
            items, end_key = self.fdb_query_items(
                partition, pk_field, sk_field, pk_value, sk_condition, sk_value, sk_second_value,
                filters, recursive_filters, max_scan_rep, start_key, limit, reverse, consistent_read
            )
            # 다음 조회에 쓰일 키 준비
            start_key = end_key
            for item in items:
                yield item
            # end_key 없으면 반복 중지
            if not end_key:
                break

    def fdb_query_items(self, partition, pk_field=None, sk_field=None, pk_value=None,
                        sk_condition=None, sk_value=None, sk_second_value=None,
                        filters=None, recursive_filters=None, max_scan_rep=100, start_key=None,
                        limit=100, reverse=False, consistent_read=False):
        """
        :param partition: 파티션 이름
        :param pk_field: 파티션 키 이름
        :param sk_field: 소트 키 이름
        :param pk_value: 파티션 키 값
        :param sk_condition: 소트 키 연산 조건
        :param sk_value: 소트 키 값
        :param sk_second_value: 소트 키 두번째 값
        :param filters: [  필터링 내용, 재귀 필터나 필터 둘 중 하나로 사용 가능, filters 는 and 만 지원함
                {
                    'field': '<FIELD>',
                    'value': '<VALUE>',
                    'condition': 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                            'is_in' | 'contains' | 'exist' | 'not_exist'
                }
            ]
        :param recursive_filters: {  재귀 필터, or, and 연산을 묶어서 수행 가능합니다. filters 대용으로 사용합니다.
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
        :param max_scan_rep: DDB 스캔시 몇번까지 반복 스캔할지 설정 (1번 스캔시 원하는 값이 안나와도 max_scan_rep번까지 반복)
        :param start_key: 이 키 값부터 탐색 시작
        :param limit: 한번에 반환할 rows 의 사이즈
        :param reverse: sk 순서가 오름차순, 내림차순 (reverse=true 일시 내림차순)
        :param consistent_read: 업데이트된 DB의 최신성을 보장하고 싶으면 true (1초 내외) 대신 연산량 더 많음.
        :return: (items, end_key)
        """
        # pk_field, value 없으면 partiton 으로 대체합니다.
        if not pk_field:
            # raise errorlist.NEED_PK_FIELD
            pk_field = '_ptn'

        if not pk_value:
            # raise errorlist.NEED_PK_VALUE
            pk_value = partition

        sort_condition = sk_condition  # 인지하기 쉽게 이름 변경함

        # 차례대로 위의 변수들이 먼저 할당되어야 쿼리할 수 있음.
        if sk_value is not None and sk_field is None:
            raise Exception('sk_field 변수가 필요합니다.')

        if sk_value is not None and sort_condition is None:
            raise Exception('sk_condition 변수가 필요합니다.')

        if sk_second_value is not None and sk_value is None:
            raise Exception('sk_value 변수가 필요합니다.')

        # sk_group 이 실제 파티션 중에 존재하는 값인지 체크, 실수 방지 차원임.
        current_partitions = self.fdb_get_partitions(use_cache=True)
        partition_object = None

        for current_partition in current_partitions:
            _partition_name = current_partition.get('_partition_name', None)
            if _partition_name == partition:
                partition_object = current_partition

        # 존재하는 파티션인지 확인
        if partition_object is None:
            raise Exception(f'{partition}: 해당 파티션이 존재하지 않습니다.')

        if not filters:
            filters = []

        if not recursive_filters:
            recursive_filters = {}

        # 요청한 필드 값들과, 실제 파티션에서 가지고 있는 값들이 매칭되는지 확인하기
        # 이 값을 기준으로 인덱스를 타게할 수 있음.
        # 파티션이나 인덱스를 다 뒤져도 맞는게 없으면 에러 레이즈
        index_name, pk_name, sk_name = _find_proper_index_name(partition_object, pk_field, sk_field)

        # start_key json 변환
        if type(start_key) is str:
            # start_key_pk, start_key_sk = resource_util.split_pk_sk(start_key)
            start_key = json.loads(start_key)

        # 최대 스캔 횟수가 있을시 반복
        scan_rep_count = 0
        if not max_scan_rep:
            max_scan_rep = 1
        items = []
        end_key = start_key

        while scan_rep_count < max_scan_rep:
            _items, end_key = self._fdb_query_items_low(
                pk_field=pk_field, pk_value=pk_value,
                sort_condition=sort_condition, partition=partition,
                sk_field=sk_field, sk_value=sk_value, sk_second_value=sk_second_value,
                start_key=end_key, filters=filters, limit=limit, reverse=reverse,
                consistent_read=consistent_read, index_name=index_name, pk_name=pk_name, sk_name=sk_name,
                recursive_filters=recursive_filters
            )
            scan_rep_count += 1
            items.extend(_items)
            if len(items) >= limit:
                break  # limit 보다 많은 경우 바로 리턴
            if not end_key:
                break

        filtered = [item for item in items if item.get('_id', None) and item.get('_ptn', None)]
        if end_key:
            end_key = json.dumps(end_key)

        filtered = [encode_dict(pop_ban_keys(item)) for item in filtered]
        return filtered, end_key

    def fdb_update_indexes(self, partition):
        # 파티션에 있는 객체들을 새로 인덱싱합니다. 오래 걸릴 수 있음.
        items = self.fdb_generate_items(partition)
        with ThreadPoolExecutor(max_workers=32) as worker:
            for idx, item in enumerate(items):
                worker.submit(self.fdb_update_item, partition, item['_id'], item)
                if idx % 1000 == 0:
                    print('update_index:', idx)

    def fdb_force_load_partitions(self, partitions):
        """
        파티션 정보들을 DB에 강제 Load 시킵니다. 위험한 API 이기 때문에 유효성 검증 확실히 필요.
        :param partitions:
        :return:
        """
        partitions_to_create = []
        # 복제, 불변성 확보
        partitions = [partition.copy() for partition in partitions]
        # 유효성 검증
        now = int(time.time())
        required_keys = [
            '_partition_name', '_pk_field', '_sk_field', '_uk_fields',
        ]
        index_required_keys = [
            '_pk_field', '_sk_field',
            'pk_name', 'sk_name',
            'index_number', 'index_name'
        ]
        if not isinstance(partitions, list):
            raise Exception('partitions must be type of list<dict>')
        for partition in partitions:
            new_partition = {}
            if not isinstance(partition, dict):
                raise Exception('a partition must be type of dict')
            for required_key in required_keys:
                if required_key not in partition:
                    raise Exception(f'a partition must have required_keys: {required_keys}')
            new_partition['_crt'] = now
            # indexes 의 형태에 대한 검사
            indexes = partition.get('indexes', [])
            for index in indexes:
                for index_required_key in index_required_keys:
                    if index_required_key not in index:
                        raise Exception(f'a index must have required_keys: {index_required_keys}')
            # _pk, _sk 만들기
            new_partition['_pk'] = config.STR_META_INFO_PARTITION
            new_partition['_sk'] = partition['_partition_name']
            new_partition['_partition_name'] = partition['_partition_name']
            new_partition['_pk_field'] = partition['_pk_field']
            new_partition['_sk_field'] = partition['_sk_field']
            new_partition['_uk_fields'] = partition['_uk_fields']
            new_partition['indexes'] = indexes
            partitions_to_create.append(new_partition)

        # 이제 실제 dump 시켜버립니다.
        self.dynamoFDB.batch_put(partitions_to_create, can_overwrite=True)
        # 파티션 캐시 삭제
        self._fdb_remove_partition_cache()
        partitions = self.fdb_get_partitions(use_cache=False)
        return partitions

    def apply_partition_map(self, fdb_partition_map):
        """
        partition_map 를 적용합니다 한방에.
        :fdb_partition_map: {
            <partition_name:str>: {
                'pk': '_ptn',  # 기본 PK
                'sk': '_crt',  # 기본 SK
                'uks': None,  # 기본 UK
                'indexes': [  # 인덱스에 넣을 항목들
                    {
                        'pk': '_ptn',
                        'sk': '_crt',
                    }, {
                        'pk': '_ptn',
                        'sk': 'phone',
                    }, {
                        'pk': '_ptn',
                        'sk': 'name',
                    },
                ]
            }, ...
        }
        :return:
        """
        # 유효성 검사
        if not isinstance(fdb_partition_map, dict):
            raise ValueError("fdb_partition_map should be a dictionary.")

        for ptn, info in fdb_partition_map.items():
            if not isinstance(ptn, str):
                raise ValueError(f"Partition name '{ptn}' should be a string.")
            if not isinstance(info, dict):
                raise ValueError(f"Info for partition '{ptn}' should be a dictionary.")
            if 'pk' not in info or 'sk' not in info:
                raise ValueError(f"Both 'pk' and 'sk' keys should be present in info for partition '{ptn}'.")
            if 'indexes' in info and not isinstance(info['indexes'], list):
                raise ValueError(f"'indexes' for partition '{ptn}' should be a list.")
            if 'indexes' in info:
                for index in info['indexes']:
                    if not isinstance(index, dict):
                        raise ValueError(f"Each index for partition '{ptn}' should be a dictionary.")
                    if 'pk' not in index or 'sk' not in index:
                        raise ValueError(
                            f"Both 'pk' and 'sk' keys should be present in each index for partition '{ptn}'.")

        origin_partitions = self.fdb_get_partitions(False)
        origin_partition_names = [origin_partition['_partition_name'] for origin_partition in origin_partitions]

        for ptn, info in fdb_partition_map.items():
            # 파티션이 없으면 생성하고, 있으면 패스.
            if ptn in origin_partition_names:
                # 있으면 pk sk 업데이트
                response = self.fdb_update_partition(ptn, info['pk'], info['sk'], info.get('uks', []))
                print('fdb_default.fdb_update_partition:', response)
            else:
                # 없으니 새로 생성
                response = self.fdb_create_partition(
                    ptn, info['pk'], info['sk'], info.get('uks', []), True
                )
                print('fdb_default.fdb_create_partition:', response)
            indexes = info.get('indexes', [])

            for index in indexes:
                pk = index['pk']
                sk = index['sk']
                try:
                    response = self.fdb_append_index(
                        ptn, pk, sk
                    )
                    print('fdb_default.fdb_append_index:', response)
                except Exception as ex:
                    print(f'Index already exist: {ex}')


class DynamoDBAPI:
    def __init__(self, group_name, credentials=None, region=shared.DEFAULT_REGION, endpoint_url=None):
        """
        :param table_name: "테이블 이름"
        :param credentials: {
            "aws_access_key_id": "str",
            "aws_secret_access_key": "str",
            "region_name": "str",
            "profile_name": "str"
        }
        :param endpoint_url: Local Server using
        """
        self.boto3_session = shared.get_boto_session(credentials)
        self.cache = {}
        self.dynamoDB = wrapper.DynamoDB(self.boto3_session, region, group_name, endpoint_url=endpoint_url)
        self.group_name = group_name

    def _wrap_table_name(self, table_name):
        # 실제 생성되는 테이블의 이름
        if self.group_name:
            return f'{self.group_name}-{table_name}'
        else:
            return table_name

    def create_table(self, table_name:str,
                        billing_mode='PAY_PER_REQUEST',
                        stream_enabled=False, stream_view_type='NEW_AND_OLD_IMAGES',
                        additional_attributes=None, additional_settings=None
                     ):
        # 쿼리 유연성을 제한하여 개발 생산성을 보장, id 파티션키로만 생성.
        response = self.dynamoDB.create_db_table(self._wrap_table_name(table_name), 'id', 'S',
                        None, None, billing_mode,
                        stream_enabled, stream_view_type,
                        additional_attributes, additional_settings)

        return response

    def create_global_index(self, table_name: str,
        partition_key: str, partition_key_type: Literal["S", "N", "B"],
        sort_key: Optional[str] = None, sort_key_type: Optional[Literal["S", "N", "B"]] = None,
        projection_type: str = "ALL",
        read_capacity_units: Optional[int] = None, write_capacity_units: Optional[int] = None,
        additional_attributes: Optional[List[Dict[str, Any]]] = None
    ):
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
        if sort_key:
            index_name = f'{partition_key}-{sort_key}'
        else:
            index_name = f'{partition_key}'
        table_name = self._wrap_table_name(table_name)
        response = self.dynamoDB.create_gsi(
            table_name, index_name, partition_key,
            partition_key_type, sort_key, sort_key_type, projection_type,
            read_capacity_units, write_capacity_units, additional_attributes
        )
        return response

    def put_item(self, table_name:str, item:Dict, can_overwrite:bool=False)->Dict:
        table_name = self._wrap_table_name(table_name)
        decoded_dict = decode_dict(item.copy())
        response = self.dynamoDB.put_item(table_name, decoded_dict, can_overwrite)
        response = encode_dict(response)
        return response

    def get_item(self, table_name: str, id: str, consistent_read: bool, use_cache: bool = False) -> Dict[str, Any]:
        """
        DynamoDB 테이블에서 아이템을 조회하는 인터페이스.
        """
        key = {
            'id': id
        }
        table_name = self._wrap_table_name(table_name)
        item = self.dynamoDB.get_item(table_name, key, consistent_read, use_cache)
        item = encode_dict(item)
        return item

    def delete_item(self,table_name: str, id: str) -> None:
        key = {
            'id': id
        }
        table_name = self._wrap_table_name(table_name)
        self.dynamoDB.delete_item(table_name, key)

    def update_item(self, table_name:str, id:str, new_item:Dict, fields_to_update: set = None)->Dict:
        """
            아이탬을 업데이트합니다.
            만약 업데이트할 항목이 DB에 없는 경우 에러가 발생합니다.
            :return:
        """
        key = {
            'id': id
        }
        table_name = self._wrap_table_name(table_name)
        new_item = {k: v for k, v in new_item.items() if k != 'id'}
        if fields_to_update is not None:
            # 이 필드만 업데이트하여 동시성 문제 해결
            new_item = {k: v for k, v in new_item.items() if k in fields_to_update}
        decoded_dict = decode_dict(new_item)
        response = self.dynamoDB.update_item(table_name, key, decoded_dict)
        updated = response.get('Attributes', {})
        return updated

    def _index_name(self, pk_field:str, sk_field:Optional[str]):
        if sk_field:
            return f'{pk_field}-{sk_field}'
        else:
            return f'{pk_field}'

    def query_items(self, table_name:str, pk_field:str, pk_value:Any,
                    sk_condition:Literal["eq", "lte", "lt", "gte", "gt", "btw", "stw"], sk_field:str, sk_value:Any,
                    sk_second_value:Any=None, filters:List[Dict[Literal["field", "condition", "value"], Any]]=None,
                    start_key:Dict=None, reverse:bool=False, limit:int=10000, consistent_read:bool=False,
                    recursive_filters:Dict=None, min_returned_item_count:Optional[int] = None)->Tuple[List[Dict], Dict]:
        """
        AWS BOTO3 전용으로 쿼리 메서드 랩핑
        :param table_name: 테이블 이름
        :param pk_field: 파티션키 속성의 이름
        :param pk_value: 파티션키 속성의 값
        :param sk_condition: 소트키 조건
        :param sk_field:
        :param sk_value:
        :param sk_second_value:
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
        :param min_returned_item_count: 이게 지정되어 있으면, 필터가 사용될때 이만큼의 아이템 건수는 반환을 보장하려고 합니다.
        :return:
        """
        index_name = self._index_name(pk_field, sk_field)
        table_name = self._wrap_table_name(table_name)
        response = self.dynamoDB.query_items(
            table_name, pk_field, pk_value, sk_condition, sk_field,
            sk_value, sk_second_value, filters, start_key, reverse, limit,
            consistent_read, index_name, recursive_filters
        )
        items = response.get('Items', [])
        end_key = response.get('LastEvaluatedKey', None)

        # 최종 반환 수가 지정되어 있는데, 그 내역을 채우지 못한 경우인데 end_key 가 존재하면 계속 반복함.
        while min_returned_item_count and min_returned_item_count > len(items) and end_key:
            response = self.dynamoDB.query_items(
                table_name, pk_field, pk_value, sk_condition, sk_field,
                sk_value, sk_second_value, filters, end_key, reverse, limit,
                consistent_read, index_name, recursive_filters
            )
            items.extend(response.get('Items', []))
            end_key = response.get('LastEvaluatedKey', None)

        items = [encode_dict(item) for item in items]
        return items, end_key

    def generate_items(self, table_name:str, pk_field:str, pk_value:Any,
                    sk_condition:Literal["eq", "lte", "lt", "gte", "gt", "btw", "stw"], sk_field:str, sk_value:Any,
                    sk_second_value:Any=None, filters:List[Dict[Literal["field", "condition", "value"], Any]]=None,
                    start_key:Dict=None, reverse:bool=False, limit:int=10000, consistent_read:bool=False,
                    recursive_filters:Dict=None):
        """
        아이템 쿼리 메소드를 제네레이터화하여 메모리를 절약
        :return:
        """
        index_name = self._index_name(pk_field, sk_field)
        table_name = self._wrap_table_name(table_name)
        response = self.dynamoDB.query_items(
            table_name, pk_field, pk_value, sk_condition, sk_field,
            sk_value, sk_second_value, filters, start_key, reverse, limit,
            consistent_read, index_name, recursive_filters
        )
        items = response.get('Items', [])
        start_key = response.get('LastEvaluatedKey', None)
        for item in items:
            yield encode_dict(item)

        while start_key:
            response = self.dynamoDB.query_items(
                table_name, pk_field, pk_value, sk_condition, sk_field,
                sk_value, sk_second_value, filters, start_key, reverse, limit,
                consistent_read, index_name, recursive_filters
            )
            items = response.get('Items', [])
            start_key = response.get('LastEvaluatedKey', None)
            for item in items:
                yield encode_dict(item)

    def put_items(self, table_name:str, items:List[Dict], can_overwrite:bool)->List[Optional[Dict]]:
        fs = []
        with ThreadPoolExecutor(max_workers=32) as worker:
            for item in items:
                f = worker.submit(self.put_item, table_name, item, can_overwrite)
                fs.append(f)
        items = [f.result() for f in fs]
        return items

    def get_items(self, table_name:str, id_list:List[str], consistent_read:bool=True)->List[Dict]:
        fs = []
        with ThreadPoolExecutor(max_workers=32) as worker:
            for _id in id_list:
                f = worker.submit(self.get_item, table_name, _id, consistent_read=consistent_read)
                fs.append(f)
        items = [f.result() for f in fs]
        return items

    def update_items(self, table_name:str, id_new_item_pairs:Dict[str, Dict])->List[Dict]:
        fs = []
        with ThreadPoolExecutor(max_workers=32) as worker:
            for _id, new_item in id_new_item_pairs.items():
                f = worker.submit(self.update_item, table_name, _id, new_item)
                fs.append(f)
        items = [f.result() for f in fs]
        return items

    def delete_items(self, table_name:str, id_list:List[str])->None:
        fs = []
        with ThreadPoolExecutor(max_workers=32) as worker:
            for _id in id_list:
                f = worker.submit(self.delete_item, table_name, _id)
                fs.append(f)
        for f in fs:
            f.result()
        return None

    def scan_items(
            self, table_name: str, start_key: Optional[dict], limit: int,
            filters:List[Dict[Literal["field", "condition", "value"], Any]]=None,
            recursive_filters: dict = None):

        table_name = self._wrap_table_name(table_name)
        response = self.dynamoDB.scan_dynamodb_table(
            table_name, filters=filters, recursive_filters=recursive_filters, start_key=start_key, limit=limit
        )
        items = response.get('Items', [])
        items = [encode_dict(item) for item in items]
        end_key = response.get('LastEvaluatedKey', None)
        return items, end_key

    def generate_scan_items(self, table_name:str, filters:List[Dict[Literal["field", "condition", "value"], Any]]=None,
                    start_key:Dict=None, limit:int=10000, recursive_filters:Dict=None):
        """
        아이템 스캔 메소드를 제네레이터화하여 메모리를 절약
        :return:
        """
        table_name = self._wrap_table_name(table_name)
        response = self.dynamoDB.scan_dynamodb_table(
            table_name, filters=filters, recursive_filters=recursive_filters, start_key=start_key, limit=limit
        )
        items = response.get('Items', [])
        start_key = response.get('LastEvaluatedKey', None)
        for item in items:
            yield encode_dict(item)

        while start_key:
            response = self.dynamoDB.scan_dynamodb_table(
                table_name, filters=filters, recursive_filters=recursive_filters, start_key=start_key, limit=limit
            )
            items = response.get('Items', [])
            start_key = response.get('LastEvaluatedKey', None)
            for item in items:
                yield encode_dict(item)

    def get_table_meta_info(self, table_name: str):
        """
        테이블 메타 정보 획득
        """
        table_name = self._wrap_table_name(table_name)
        response = self.dynamoDB.get_table_meta_info(table_name)
        return response

    def list_group_table_names(self) -> list[str]:
        """
        GroupName 으로 시작하는 테이블 이름 리스트 반환
        :return:
        """
        all_tables = []
        last_evaluated_table = None

        while True:
            response = self.dynamoDB.get_table_names(last_evaluated_table=last_evaluated_table)
            all_tables.extend(response.get('TableNames', []))

            # 마지막 페이지면 종료
            if 'LastEvaluatedTableName' not in response:
                break
            # 다음 페이지 조회를 위해 마지막 테이블 이름 저장
            last_evaluated_table = response['LastEvaluatedTableName']
        # group_name 으로 시작하는것만 반환함.
        all_tables = [all_table.replace(f'{self.group_name}-', '') for all_table in all_tables if all_table.startswith(self.group_name)]
        return all_tables

    def get_stream_arn(self, table_name: str) -> Optional[str]:
        # DynamoDB 스트림 ARN 가져오기
        table_name = self._wrap_table_name(table_name)
        stream_arn = self.dynamoDB.get_stream_arn(table_name)
        return stream_arn

    def set_stream_enabled(self, table_name: str, stream_enabled: bool, stream_view_type: str = 'NEW_AND_OLD_IMAGES'):
        """
        스트림 활성여부 지정
        """
        table_name = self._wrap_table_name(table_name)
        return self.dynamoDB.set_stream_enabled(table_name, stream_enabled, stream_view_type=stream_view_type)

    def get_stream_enabled(self, table_name: str) -> bool:
        """
        스트림 활성 여부
        """
        table_name = self._wrap_table_name(table_name)
        return self.dynamoDB.get_stream_enabled(table_name)