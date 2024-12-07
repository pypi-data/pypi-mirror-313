#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from openai import OpenAI
from openai import OpenAI, APIStatusError

client = OpenAI(
    api_key="c3de8e16-cba7-4c60-a2f6-a2c9dfc95540",
    base_url="https://ark.cn-beijing.volces.com/api/v3", # /chat/completions
)

try:
    completion = client.chat.completions.create(
        model="ep-20240515073409-dlpqp",
        messages=[
            {"role": "user", "content": "画条狗出来 返回图片"}
        ],
        # top_p=0.7,
        top_p=None,
        temperature=None,
        stream=False,
        stream_options={"include_usage": True},
        max_tokens=6000
    )
except APIStatusError as e:
    print(e.status_code)

    print(e.response)
    print(e.message)
    print(e.code)

for chunk in completion:
    print(chunk.choices[0].delta.content)

