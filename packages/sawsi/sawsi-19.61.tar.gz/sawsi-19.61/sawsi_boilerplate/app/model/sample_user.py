"""
This is sample code to tell how to use sawsi framework.
You could delete this file after know how to use this framework.
"""

import time
import uuid
import api
from pydantic import fields, BaseModel
from typing import Optional, Literal, TypeVar, Generic, Type
from sawsi.model.base import DynamoModel, sync


class Address(BaseModel):
    street: str
    city: str
    country: str


@sync
class User(DynamoModel):
    __dynamo__ = api.dynamo
    __create_default_index__ = True  # Optional 이며, 파티션 키 부하에 민감한 경우 전체 쿼리를 위한 인덱스를 제거하는데 사용됨.
    _table = 'user'
    _indexes = [
        ('gender', 'crt'),
        ('gender', 'name'),
    ]

    id: str = fields.Field(default_factory=lambda: str(uuid.uuid4()))
    crt:float = fields.Field(default_factory=time.time)
    ptn:str = 'user'
    name: str
    age: int
    gender: Optional[Literal["male", "female"]] = None
    address: Address

    def view(self)->dict:
        return {
            'name': self.name,
            'age': self.age
        }


if __name__ == '__main__':
    # 모델 인스턴스 생성
    address_data = {'street': '123 Main St', 'city': 'Anytown', 'country': 'USA'}
    user_data = {'name': 'John Doe', 'age': 30, 'gender': 'male', 'address': address_data}
    user = User(**user_data)
    print('user.id', user.id)

    # 모델을 딕셔너리로 변환
    user_dict = user.model_dump()
    print(user_dict)
