#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : contextmanagers
# @Time         : 2024/1/9 08:36
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from contextlib import contextmanager, asynccontextmanager


@contextmanager
def timer(task="Task"):
    """https://www.kaggle.com/lopuhin/mercari-golf-0-3875-cv-in-75-loc-1900-s
        # 其他装饰器可学习这种写法
        with timer() as t:
            time.sleep(3)

        @timer()
        def f():
            print('sleeping')
            time.sleep(6)
            return 6
    """

    logger.info(f"{task} started")
    s = time.perf_counter()
    yield
    e = time.perf_counter()
    logger.info(f"{task} done in {e - s:.3f} s")


@contextmanager
def try_catcher(task="Task", fallback: Callable = None, is_trace: bool = False):
    try:
        yield
    except Exception as e:
        error = traceback.format_exc() if is_trace else e
        logger.error(f"{task}: {error}")
        if fallback:
            yield fallback()


@asynccontextmanager
async def atry_catcher(task="Task", fallback: Callable = None, is_trace: bool = False):
    try:
        yield
    except Exception as e:
        error = traceback.format_exc() if is_trace else e
        logger.error(f"{task}: {error}")
        if fallback:
            yield await fallback()


if __name__ == '__main__':
    async def f():
        return 1/0


    with try_catcher("test"):
        arun(f())
