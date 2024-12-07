#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2024/8/19 14:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from openai import OpenAI, AsyncOpenAI

chat = OpenAI().chat.completions.create
achat = AsyncOpenAI().chat.completions.create
