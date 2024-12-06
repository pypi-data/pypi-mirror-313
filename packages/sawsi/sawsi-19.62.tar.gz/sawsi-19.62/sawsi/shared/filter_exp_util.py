import json
from typing import Literal


class Exp:
    def __init__(self, field, condition: Literal['eq', 'neq', 'lte', 'lt', 'gte', 'gt', 'btw', 'stw', 'is_in', 'contains', 'exist', 'not_exist'],
                 value):
        """
        DynamoDB Filter Expression (Recursive Version)
        :param field:
        :param value:
        :param condition: 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                        'is_in' | 'contains' | 'exist' | 'not_exist'
        :param operation:
        :param left:
        :param right:
        """
        allow_conditions = {'eq', 'neq', 'lte', 'lt', 'gte', 'gt', 'btw', 'stw', 'is_in', 'contains', 'exist', 'not_exist'}

        if condition not in allow_conditions:
            raise Exception(f"condition(={condition}) not in {allow_conditions}")

        self.field = field
        self.value = value
        self.condition = condition
        self.operation = None
        self.left = None
        self.right = None

    def to_dict(self):
        if self.operation:
            return {
                'left': self.left.to_dict(),
                'operation': self.operation,
                'right': self.right.to_dict(),
            }
        else:
            return {
                'field': self.field,
                'value': self.value,
                'condition': self.condition,
            }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)

    def or_(self, other):
        exp = Exp(None, 'eq', None)
        exp.condition = None
        exp.operation = 'or'
        exp.left = self
        exp.right = other
        return exp

    def and_(self, other):
        exp = Exp(None, 'eq', None)
        exp.condition = None
        exp.operation = 'and'
        exp.left = self
        exp.right = other
        return exp


if __name__ == '__main__':
    # Example usage
    expression = Exp('name1', 'contains', 'value1').or_(
        Exp('name2', 'contains', 'value2').and_(
            Exp('name3', 'contains', 'value3')
        )
    )

    print(expression)
