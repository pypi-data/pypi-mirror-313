import traceback
import datetime
from croniter import croniter
from concurrent.futures import ThreadPoolExecutor


pool = ThreadPoolExecutor(max_workers=8)
futures = []


def join():
    for future in futures:
        future.result()


def try_run(func, *args, **kwargs):
    return func(*args, **kwargs)


class ScheduledTask:
    def __init__(self, cron_expression):
        self.cron_expression = cron_expression

    def __enter__(self):
        now = datetime.datetime.now() + datetime.timedelta(seconds=5)
        iter = croniter(self.cron_expression, now)
        prev_schedule = iter.get_prev(datetime.datetime)

        if not (prev_schedule.year == now.year and prev_schedule.month == now.month and
                prev_schedule.day == now.day and prev_schedule.hour == now.hour and
                prev_schedule.minute == now.minute):
            def run(*args, **kwargs):
                class Empty:
                    @classmethod
                    def result(cls):
                        pass
                return Empty
            return run

        def run(*args, **kwargs):
            global futures, pool
            future = pool.submit(try_run, *args, **kwargs)
            futures.append(future)
            return future
        return run

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            traceback_str = ''.join(traceback.format_exception(exc_type, exc_val, exc_tb))
            self.handle_error(exc_val, traceback_str)
            return True  # 에러를 처리하고 정상 종료

    def handle_error(self, exc_val, exc_tb):
        # 에러 처리 로직
        message = f'Error on scheduler: {exc_val}, {exc_tb}'
        raise RuntimeError(message)



if __name__ == '__main__':
    raise RuntimeError('pk')