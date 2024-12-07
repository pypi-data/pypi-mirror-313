#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2024/6/14 10:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import time
from functools import lru_cache, wraps


def ttl_fn(ttl: int = 60):
    return time.time() // ttl  # 缓存时间


def lru_cache_with_ttls(maxsize=128, typed: bool = False, ttl: Optional[int] = None):
    cache = lru_cache(maxsize, typed)

    @wrapt.decorator  # 主逻辑
    def inner(wrapped, instance, args, kwargs):

        @cache
        def _wrapped(_ttl):
            return wrapped(*args, **kwargs)

        return _wrapped(ttl_fn(ttl))

    return inner


def lru_cache_with_ttl(maxsize=128, typed: bool = False, ttl: Optional[int] = None):
    def decorator(func):
        # 使用lru_cache作为基础缓存机制
        lru = lru_cache(maxsize=maxsize)(func)
        lru_cache_data = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key = args + tuple(kwargs.items())

            # 检查是否在缓存中以及是否过期
            if key in lru_cache_data:
                entry, timestamp = lru_cache_data[key]
                if time.time() - timestamp < ttl:
                    return entry
                else:
                    # 如果过期，删除缓存
                    del lru_cache_data[key]

            # 调用原始函数并缓存结果
            result = lru(*args, **kwargs)
            lru_cache_data[key] = (result, time.time())
            return result

        # 使用lru_cache的缓存信息函数
        wrapper.cache_info = lru.cache_info
        wrapper.cache_clear = lru.cache_clear
        return wrapper

    return decorator


# 示例使用


if __name__ == '__main__':
    @lru_cache_with_ttls(maxsize=128, ttl=3)
    def expensive_function(n):
        logger.debug("不走缓存")
        return n


    print(expensive_function(11))
    print(expensive_function(11))
    time.sleep(5)
    print(expensive_function(11))
