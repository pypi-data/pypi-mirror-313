#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : HermesCache_tes
# @Time         : 2024/12/6 10:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://hermescache.readthedocs.io/en/latest/
import asyncio

from meutils.pipe import *
import hermes.backend.redis

cache = hermes.Hermes(
    hermes.backend.redis.Backend,
    ttl=600,
    host='localhost',
    db=1,
)

hermes.Serialiser


@cache
def foo(a, b):
    return a * b

@cache
async def func(x):
    await asyncio.sleep(5)
    logger.debug('异步函数')
    return x


class Example:

    @cache(tags=('math', 'power'), ttl=1200)
    def bar(self, a, b):
        return a ** b

    @cache(tags=('math', 'avg'), key=lambda fn, a, b: f'avg:{a}:{b}')
    def baz(self, a, b):
        return (a + b) / 2


print(foo(2, 333))

example = Example()
print(example.bar(2, 10))
print(example.baz(2, 10))

foo.invalidate(2, 333)
example.bar.invalidate(2, 10)
example.baz.invalidate(2, 10)

cache.clean(['math'])  # invalidate entries tagged 'math'
cache.clean()  # flush cache


if __name__ == '__main__':
    class Request(BaseModel):
        a: str = "a"

        class Config:
            frozen = True
    arun(func(1))