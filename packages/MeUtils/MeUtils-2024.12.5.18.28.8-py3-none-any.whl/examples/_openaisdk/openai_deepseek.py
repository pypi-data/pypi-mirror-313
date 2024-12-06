#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_moon
# @Time         : 2024/6/14 17:27
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://api.moonshot.cn/v1/users/me/balance get查余额


from meutils.pipe import *
from openai import OpenAI

base_url = os.getenv('DEEPSEEK_BASE_URL')
api_key = os.getenv('DEEPSEEK_API_KEY')
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

completion = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "1+1"},
    ],
)

print(completion)
