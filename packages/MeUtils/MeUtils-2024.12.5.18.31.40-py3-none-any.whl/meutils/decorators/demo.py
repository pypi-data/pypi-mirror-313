#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2021/4/2 3:54 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.decorators.feishu import *

from meutils.decorators.retry import retrying
import asyncio

import openai

@retrying
async def my_coroutine_function():
    # 在这里执行协程函数的逻辑
    # 如果发生异常，tenacity将自动重试
    await asyncio.sleep(1)
    raise Exception("Something went wrong")

async def main():
    try:
        await my_coroutine_function()
    except Exception as e:
        print(f"Exception: {e}")

asyncio.run(main())