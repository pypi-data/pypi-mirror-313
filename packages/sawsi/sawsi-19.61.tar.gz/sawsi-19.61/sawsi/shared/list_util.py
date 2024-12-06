"""
list 객체 관련 유틸
"""


def divide_chunks(l, n):
    # 입력된 리스트 l 을 n 개씩 갖도록 split
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
