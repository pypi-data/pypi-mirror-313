"""
집합관련 유틸
"""


class HashableDict(dict):
    # hash 로 쓸 dict 의 field 를 지정할 수 있음
    def __init__(self, dict_object, keys_to_hash):
        self.__keys_to_hash = keys_to_hash
        super().__init__(dict_object)

    def __hash__(self):
        return hash(self._make_hash_str())

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def _make_hash_str(self):
        return '|'.join([str(self.get(key, '')) for key in self.__keys_to_hash])


if __name__ == '__main__':
    d1 = {1: 2, 3: 5}
    d2 = {1: 2, 4: 7}
    d1 = HashableDict(d1, [1])
    d2 = HashableDict(d2, [2])
    s = {d1, d2}
    print(s)