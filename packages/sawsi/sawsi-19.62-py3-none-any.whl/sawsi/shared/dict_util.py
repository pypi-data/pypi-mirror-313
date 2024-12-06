"""
dict 관련 유틸
"""
import json
from decimal import Decimal


def convert_number_to_decimal(dict_detail):
    for key, value in dict_detail.items():
        if isinstance(value, float):
            dict_detail[key] = Decimal(str(value))
        elif isinstance(dict_detail[key], dict):
            convert_number_to_decimal(dict_detail[key])
        elif isinstance(dict_detail[key], list):
            for item in dict_detail[key]:
                if isinstance(item, dict):
                    convert_number_to_decimal(item)
    return dict_detail


def convert_decimal_to_number(dict_detail):
    for key, value in dict_detail.items():
        if isinstance(value, Decimal):
            if value % 1 == 0:
                dict_detail[key] = int(value)
            else:
                dict_detail[key] = float(value)
        elif isinstance(dict_detail[key], dict):
            convert_decimal_to_number(dict_detail[key])
        elif isinstance(dict_detail[key], list):
            for item in dict_detail[key]:
                if isinstance(item, dict):
                    convert_decimal_to_number(item)
    return dict_detail



def _convert_dynamodb_json(dynamodb_json):
    if isinstance(dynamodb_json, dict):
        if 'S' in dynamodb_json:
            return dynamodb_json['S']
        elif 'N' in dynamodb_json:
            return float(dynamodb_json['N']) if '.' in str(dynamodb_json['N']) else int(dynamodb_json['N'])
        elif 'M' in dynamodb_json:
            return {k: _convert_dynamodb_json(v) for k, v in dynamodb_json['M'].items()}
        elif 'L' in dynamodb_json:
            return [_convert_dynamodb_json(v) for v in dynamodb_json['L']]
        elif 'BOOL' in dynamodb_json:
            return dynamodb_json['BOOL']
        elif 'NULL' in dynamodb_json:
            return None
    return dynamodb_json


def convert_dynamodb_document_to_dict(document: dict):
    return {key: _convert_dynamodb_json(value) for key, value in document.items()}


if __name__ == '__main__':
    # r = get_value_by_dot_representation({'a': {'b': {'c': {'d': 'e'}}}}, 'a')
    # print(r)
    print(convert_number_to_decimal({
        'd': {
            'd': {
                '1': 14.232,
                'd': 'ss'
            },
            's': {
                'g': 'sss'
            },
            'ss': [
                {
                    'ok': 1.141,
                    'ss': 'ssss'
                }
            ]
        }
    }))