from pydantic import BaseModel, fields, validate_call
from pydantic.fields import PydanticUndefined
from typing import TypeVar, Generic, Type, Dict, Tuple, Optional
from typing import Literal, get_origin, get_args, Union, Any, List, Iterator
import uuid, time
from sawsi.shared.filter_exp_util import Exp
from concurrent.futures import ThreadPoolExecutor
import importlib
import pkgutil

__models_to_sync__ = []

def sync(cls):
    # 위 데코레이터를 가지고 있는 클래스들은 build_keeper.py 에서 동기화합니다.
    __models_to_sync__.append(cls)
    return cls

@validate_call
def sync_all_models(package_names: List[str]):
    """
    sync 데코레이터가 적용된 모든 클래스의 sync_table 메서드를 호출할 수 있습니다.
    :param package_names:
    :return:
    """
    for package_name in package_names:
        # 패키지를 import합니다. 이는 동적으로 모듈 경로에 따라 달라집니다.
        package = importlib.import_module(package_name)

        # 주어진 패키지 경로에서 모든 모듈을 순회하며 import합니다.
        for (_, module_name, _) in pkgutil.iter_modules(package.__path__, package_name + '.'):
            importlib.import_module(module_name)
    # 예를 들어, main.model 패키지 내의 모든 모듈을 동기화합니다.
    # 데코레이터가 적용된 모든 클래스의 메서드를 호출할 수 있습니다.
    # 총 24개의 테이블이 동시 생성이 가능함
    with ThreadPoolExecutor(max_workers=24) as worker:
        for cls in __models_to_sync__:
            # 기본 u_b 인덱스 생성 여부입니다.
            try:
                create_default_index = getattr(cls, '__create_default_index__', True)
                worker.submit(cls.sync_table, create_default_index)
            except Exception as ex:
                # 메소드가 없을때 호출될 수 있음
                print(ex)


# 현재 클래스 형을 나타내는 TypeVar 생성
T = TypeVar('T', bound='DynamoModel')
cache = {}

class DynamoModel(BaseModel, Generic[T]):
    id: str = fields.Field(default_factory=lambda: str(uuid.uuid4()))
    crt: float = fields.Field(default_factory=lambda: float(time.time()))
    u_b:str = '_'  # 파티션 쿼리용

    @classmethod
    def get_fields_with_default_values(cls) -> List[str]:
        fields_with_defaults = []
        for name, field in cls.model_fields.items():
            if field.default is not PydanticUndefined or field.default_factory is not None:
                fields_with_defaults.append(name)
        return fields_with_defaults

    def __init__(self, **data):
        super().__init__(**data)
        self.__initial_values__ = self.model_dump()
        self.__modified_attributes__ = set()

    def __setattr__(self, name, value):
        if name in self.model_fields:
            # 수정되면 다 추가
            self.__modified_attributes__.add(name)
        super().__setattr__(name, value)

    def get_attributes_to_update(self):
        # 수정된거 + 기본값 있는 필드들
        now_values = self.model_dump()
        for key, value in now_values.items():
            if key not in self.__initial_values__:
                self.__modified_attributes__.add(key)
            elif self.__initial_values__[key] != value:
                self.__modified_attributes__.add(key)
        return list(self.__modified_attributes__)

    @classmethod
    def _table_name(cls):
        return cls._table.get_default()

    @classmethod
    def get(cls: Type[T], id: str, consistent_read: bool = True, use_cache: bool = False) -> Optional[T]:
        """
        아이템을 가져와 객체로 반환합니다.
        :param id: item.id
        :param consistent_read:
        :param use_cache:
        :return:
        """
        data = cls.__dynamo__.get_item(
            cls._table_name(), id, consistent_read, use_cache
        )
        if data:
            return cls(**data)
        else:
            return None

    @classmethod
    def validate_model(cls, my_model):
        # 클래스화하여 모델 검증
        data = my_model.model_dump()
        return cls(**data)

    @classmethod
    def batch_get(cls: Type[T], id_list: List[str], consistent_read: bool = True, use_cache: bool = False) -> List[Optional[T]]:
        items = []
        futures = []
        with ThreadPoolExecutor(max_workers=32) as worker:
            for item_id in id_list:
                future = worker.submit(cls.__dynamo__.get_item, cls._table_name(), item_id, consistent_read, use_cache)
                futures.append(future)
        for future in futures:
            data = future.result()
            if data:
                items.append(cls(**data))
            else:
                items.append(None)
        return items

    def put(self: Type[T], can_overwrite: bool=False)->Dict:
        """
        Save (create) item to DB
        :return:
        """
        self.validate_model(self)
        data = self.__dynamo__.put_item(
            self._table_name(), self.model_dump(), can_overwrite
        )
        return self

    def update(self: Type[T], force_update_default_fields: bool = False) -> T:
        """
        Update item to DB with state of this instance
        force_update_default_fields: 기본값 가진 필드는 업데이트 대상에 무조건 포함시킴
        :return:
        """
        attributes_to_update = self.get_attributes_to_update()
        if force_update_default_fields:
            default_fields = self.get_fields_with_default_values()  # 기본값 있는 필드는 비교가 불가능하기 때문에
            attributes_to_update += default_fields

        if attributes_to_update:
            self.validate_model(self)
            # 수정된게 있는 경우만 업데이트 진행함
            updated = self.__dynamo__.update_item(
                self._table_name(), self.id, self.model_dump(), self.get_attributes_to_update()
            )
        return self

    def delete(self: Type[T]) -> None:
        """
        Delete Item
        :return:
        """
        self.__dynamo__.delete_item(
            self._table_name(), self.id
        )

    @classmethod
    def generate(cls: Type[T], pk_field:Optional[str]='u_b', pk_value:Any='_',
                    sk_condition:Literal["eq", "lte", "lt", "gte", "gt", "btw", "stw"]=None,
                    sk_field:Optional[str]=None, sk_value:Any=None,
                    sk_second_value:Any=None,
                    start_key:Dict=None, reverse:bool=False, limit:int=10000, consistent_read:bool=True,
                    filter_expression:Exp=None) -> Iterator[T]:
        """
        Query and get all items by generator
        :param pk_field: Field name to query (EX: 'user_id')
        :param pk_value: Field value to query (EX: 'uui21-sqtx54-er2367-jsk36s')
        :param sk_condition: Sort key condition Literal["eq", "lte", "lt", "gte", "gt", "btw", "stw"]
        :param sk_field: Sort key field name to query (EX: 'crt')
        :param sk_value: Sort key field value to query with sk_condition (EX: 1645437454) [Non-required]
        :param sk_second_value: If you want to use sk_condition "btw" (between), You can query like "sk_value <= sk_field <= sk_second_value" [Non-required]
        :param start_key:
        :param reverse:
        :param limit:
        :param consistent_read:
        :param filter_expression: Exp instance EX:
        You can "from sawsi.model.base import Exp" and, Use
        Exp(field='name', value='kim', condition='eq').or_(
            Exp(field='name', value='lee', condition='eq')
        )
        :return:
        """
        recursive_filters = None
        if filter_expression:
            recursive_filters = filter_expression.to_dict()

        if pk_field is None:
            # 파티션 키 지정 안한 경우
            pk_field = 'u_b'
            pk_value = '_'

        if pk_field == 'u_b' and pk_value == '_' and not sk_field:
            # Default index set
            sk_field = 'crt'

        if sk_field is not None and sk_value is not None and sk_condition is None:
            # value 가 있는데 조건이 없으면
            sk_condition = 'eq'

        gen = cls.__dynamo__.generate_items(
            cls._table_name(), pk_field=pk_field, pk_value=pk_value,
            sk_condition=sk_condition, sk_field=sk_field, sk_value=sk_value, sk_second_value=sk_second_value,
            start_key=start_key, reverse=reverse, limit=limit, consistent_read=consistent_read,
            recursive_filters=recursive_filters
        )
        for data in gen:
            yield cls(**data)

    @classmethod
    def query(cls: Type[T], pk_field:Optional[str]='u_b', pk_value:Any='_',
                    sk_condition:Literal["eq", "lte", "lt", "gte", "gt", "btw", "stw"]=None,
                    sk_field:Optional[str]=None, sk_value:Any=None,
                    sk_second_value:Any=None, filters:List[Dict[Literal["field", "condition", "value"], Any]]=None,
                    start_key:Optional[Dict]=None, reverse:bool=False, limit:int=10000, consistent_read:bool=True,
                    filter_expression:Exp=None, min_returned_item_count:Optional[int] = None) -> Tuple[List[T], dict]:
        recursive_filters = None
        if filter_expression:
            recursive_filters = filter_expression.to_dict()

        if pk_field is None:
            # 파티션 키 지정 안한 경우
            pk_field = 'u_b'
            pk_value = '_'

        if pk_field == 'u_b' and pk_value == '_' and not sk_field:
            # Default index set
            sk_field = 'crt'

        if sk_field is not None and sk_value is not None and sk_condition is None:
            # value 가 있는데 조건이 없으면
            sk_condition = 'eq'

        datas, end_key = cls.__dynamo__.query_items(
            cls._table_name(), pk_field=pk_field, pk_value=pk_value,
            sk_condition=sk_condition, sk_field=sk_field, sk_value=sk_value, sk_second_value=sk_second_value,
            filters=filters,
            start_key=start_key, reverse=reverse, limit=limit, consistent_read=consistent_read,
            recursive_filters=recursive_filters, min_returned_item_count=min_returned_item_count
        )
        return [cls(**data) for data in datas], end_key

    @classmethod
    def scan(cls: Type[T], start_key: Optional[Dict] = None, limit: int = 100000,  filter_expression: Exp = None) -> Iterator[T]:
        """
        Query and get all items by generator
        :param start_key:
        :param limit:
        :param filter_expression: Exp instance EX:
        You can "from sawsi.model.base import Exp" and, Use
        Exp(field='name', value='kim', condition='eq').or_(
            Exp(field='name', value='lee', condition='eq')
        )
        :return:
        """
        recursive_filters = None
        if filter_expression:
            recursive_filters = filter_expression.to_dict()
        gen = cls.__dynamo__.generate_scan_items(
            cls._table_name(),
            start_key=start_key, limit=limit, recursive_filters=recursive_filters
        )
        for data in gen:
            yield cls(**data)

    @classmethod
    def sync_table(cls, create_default_index=True):
        """
        테이블이 없으면 생성, 인덱스도 없으면 생성합니다.
        :return:
        """
        try:
            cls.__dynamo__.create_table(cls._table_name())
            if create_default_index:
                # 기본 u_ index (파티션 정렬 쿼리용)
                cls.__dynamo__.create_global_index(
                    cls._table_name(),
                    'u_b', 'S',
                    'crt', 'N'
                )
            for partition_key, sort_key in cls._indexes.get_default():
                if not partition_key:
                    # None 이거나 없으면 기본 전체 인덱스로 설정함.
                    partition_key = 'u_b'

                partition_key_type = extract_dynamodb_type(cls.model_fields[partition_key].annotation)
                if sort_key:
                    sort_key_type = extract_dynamodb_type(cls.model_fields[sort_key].annotation)
                    cls.__dynamo__.create_global_index(
                        cls._table_name(),
                        partition_key, partition_key_type,
                        sort_key, sort_key_type
                    )
                else:
                    cls.__dynamo__.create_global_index(
                        cls._table_name(),
                        partition_key, partition_key_type,
                    )
        except Exception as ex:
            print(ex)


    @classmethod
    def sync_table_only(cls):
        """
        테이블이 없으면 생성
        :return:
        """
        cls.__dynamo__.create_table(cls._table_name())

    @classmethod
    def sync_indexes_only(cls, create_default_index: bool = True):
        if create_default_index:
            # 기본 u_ index (파티션 정렬 쿼리용)
            cls.__dynamo__.create_global_index(
                cls._table_name(),
                'u_b', 'S',
                'crt', 'N'
            )
        for partition_key, sort_key in cls._indexes.get_default():
            if not partition_key:
                # None 이거나 없으면 기본 전체 인덱스로 설정함.
                partition_key = 'u_b'

            partition_key_type = extract_dynamodb_type(cls.model_fields[partition_key].annotation)
            if sort_key:
                sort_key_type = extract_dynamodb_type(cls.model_fields[sort_key].annotation)
                cls.__dynamo__.create_global_index(
                    cls._table_name(),
                    partition_key, partition_key_type,
                    sort_key, sort_key_type
                )
            else:
                cls.__dynamo__.create_global_index(
                    cls._table_name(),
                    partition_key, partition_key_type,
                )

    def __hash__(self):
        return hash(self._make_hash_str())

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def _make_hash_str(self):
        return str(self.id)

    @classmethod
    def get_table_meta_info(cls):
        response = cls.__dynamo__.get_table_meta_info(
            cls._table_name()
        )
        return response


def extract_dynamodb_type(annotation) -> str:
    """
    Pydantic annotation 을 DDB Attr Type 으로 변환합니다.
    :param annotation:
    :return:
    """
    # Optional 타입 처리
    if get_origin(annotation) is Union:
        args = get_args(annotation)
        # Optional[X]는 Union[X, NoneType]과 같으므로, NoneType을 제외하고 처리
        non_none_args = [arg for arg in args if arg is not type(None)]
        if len(non_none_args) == 1:
            return extract_dynamodb_type(non_none_args[0])

    # Literal 타입 처리
    if get_origin(annotation) is Literal:
        # Literal 내부의 모든 값이 문자열이면 'S', 그렇지 않으면 예외 처리
        args = get_args(annotation)
        if all(isinstance(arg, str) for arg in args):
            return 'S'
        else:
            raise ValueError("DynamoDB does not support this kind of Literal directly.")

    # 기본 타입 처리
    if annotation is int or annotation is float:
        return 'N'
    elif annotation is str:
        return 'S'
    elif annotation is bytes:
        return 'B'

    # 지원되지 않는 타입
    raise ValueError(f"Unsupported type annotation: {annotation}")
