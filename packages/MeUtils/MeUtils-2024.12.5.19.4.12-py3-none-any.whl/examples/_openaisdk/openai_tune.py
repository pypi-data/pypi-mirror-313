#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat_tune
# @Time         : 2024/9/20 20:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :




from meutils.pipe import *
from openai import OpenAI

client = OpenAI(

)

completion = client.chat.completions.create(
    # model="anthropic/claude-3.5-sonnet",
    # model="openai/gpt-4o-mini",
    # model="openai/gpt-4o",
    # model="anthropic/claude-3.5-sonnet",
    # model="gpt-4o-mini",
    model="gpt-4-turbo",

    messages=[
        {"role": "user", "content": "1+1"},
    ],
    max_tokens=10000
)

print(completion)
