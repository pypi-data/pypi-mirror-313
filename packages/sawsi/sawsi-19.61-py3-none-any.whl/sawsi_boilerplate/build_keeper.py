"""
빌드 준비에 필요한 코드 호출
샘플입니다. 적절히 변경해서 사용해주세요.
"""


import api
import config
import traceback
from {{app}}.model.sample_user import Address, User
from sawsi.model.base import sync_all_models


def run():
    config.build = True
    # DB 초기화 등 진행.

    sync_all_models([
        "{{app}}.model"
    ])
    api.locking.init_table()
    api.firehose_log.init()
    api.s3_public.init_s3_bucket()
    # 초기화 메서드를 제공하지 않는 리소스는, AWS Console 에서 직접 생성 요망

    if config.env == 'dev':
        import {{app}}.doc_maker
        {{app}}.doc_maker.make_api_doc()


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        raise Exception(f'Exception:{e}, \ntraceback:{traceback.format_exc()}')
        # 에러를 다시 발생시켜 CodeBuild가 실패 상태를 감지할 수 있도록 합니다.
