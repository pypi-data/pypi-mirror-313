#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from openai import OpenAI

client = OpenAI(
    # api_key=os.getenv("SILICONFLOW_API_KEY"),
    api_key="sk-zhvfnyebjcrylrwwzecxcbolwdsitqfwjqzxeysqhprdsjbm",
    base_url="https://api.siliconflow.cn/v1",
)

# print(client.models.list())


model = "01-ai/Yi-1.5-6B-Chat"
# model = "THUDM/glm-4-9b-chat"
# model = "google/gemma-2-9b-it"
# model = "internlm/internlm2_5-7b-chat"
# model = "google/gemma-2-27b-it"
# model = 'chat-kolors'
# model = "deepseek-ai/DeepSeek-V2-Chat"
# model = "meta-llama/Meta-Llama-3.1-8B-Instruct"
# model = "meta-llama/Meta-Llama-3.1-70B-Instruct"
# model = 'meta-llama/Meta-Llama-3.1-405B-Instruct'

# api black-forest-labs/FLUX.1-schnell
messages = [
    {'role': 'user', 'content': '你是谁'}
]
response = client.chat.completions.create(
    # model='alibaba/Qwen1.5-110B-Chat',
    model=model,
    # messages=[
    #     {'role': 'user', 'content': "抛砖引玉是什么意思呀"}
    # ],
    messages=messages,
    stream=True,
    max_tokens=2048,
)
print(response)
for chunk in response:
    print(chunk.choices[0].delta.content)
