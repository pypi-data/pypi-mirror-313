
SK_DIGIT_FIT = 20  # sort key 의 자리 맞춤 총 문자열 개수임.
SK_FLOAT_DEC_FIT = 16  # SK_DIGIT_FIT 에서 소숫점 자리가 차지하는 부분, 데시멀 (10진수)임

# base64 'z' * SK_DIGIT_FIT 로 표현할 수 있는 최대 범위 // 2
HALF_REP_NUMBER_B64 = 664613997892457936451903530140172288
MAX_REP_NUMBER_B64 = HALF_REP_NUMBER_B64 * 2

# 숫자를 base64 형태로 변환하여 표현
BASE64_LETTERS = "+/0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
STR_META_INFO_PARTITION = 'meta-info#partition'
END_NOTATION = '|'


if __name__ == '__main__':
    print(64**20 // 2)