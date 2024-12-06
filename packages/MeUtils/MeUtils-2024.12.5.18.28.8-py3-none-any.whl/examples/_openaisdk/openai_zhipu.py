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
    # api_key="e21bd630f681c4d90b390cd609720483.WSFVgA3KkwNCX0mN",
    # base_url="https://open.bigmodel.cn/api/paas/v4/"

    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3YmFmYWQzYTRmZDU0OTk3YjNmYmNmYjExMjY5NThmZiIsImV4cCI6MTczODAyNDg4MiwibmJmIjoxNzIyNDcyODgyLCJpYXQiOjE3MjI0NzI4ODIsImp0aSI6IjY5Y2ZiNzgzNjRjODQxYjA5Mjg1OTgxYmY4ODMzZDllIiwidWlkIjoiNjVmMDc1Y2E4NWM3NDFiOGU2ZmRjYjEyIiwidHlwZSI6InJlZnJlc2gifQ.u9pIfuQZ7Y00DB6x3rbWYomwQGEyYDSE-814k67SH74",
    base_url="https://any2chat.chatfire.cn/glm/v1"
)

# try:
#     completion = client.chat.completions.create(
#         model="glm-4",
#         messages=[
#             {"role": "system", "content": "你是个画图工具"},
#             {"role": "user", "content": "画条狗出来 返回图片"}
#         ],
#         # top_p=0.7,
#         top_p=None,
#         temperature=None,
#         stream=False,
#         max_tokens=6000
#     )
# except APIStatusError as e:
#     print(e.status_code)
#
#     print(e.response)
#     print(e.message)
#     print(e.code)
#
# for chunk in completion:
#     print(chunk.choices[0].delta.content)

r = client.images.generate(
    model="cogview-3-plus",
    prompt="a white siamese cat",
    size="1024x1024",
    quality="hd",
    n=1,
)
