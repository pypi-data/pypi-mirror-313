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

client = OpenAI(
api_key="sk-iPNbgHSRkQ9VUb6iAcCa7a4539D74255A6462d29619d6519",
    # api_key='sk-Gqbp2zoc71gWBVxvBd23D89f469e4e78A823357e2e625455',

    # api_key=os.getenv("SILICONFLOW_API_KEY"),
    # # api_key="sk-gcxjtocodgggxwnhqqsaqznpkpxndktwlgmgkmzljyajjsfp",
    # base_url="https://api.siliconflow.cn/v1",

    # base_url="https://api.bltcy.ai/v1"
)

model = "BAAI/bge-large-zh-v1.5"
model = "bge-large-zh-v1.5"
model = "text-embedding-3-small"
model = "text-embedding-ada-002"
#
# model = "BAAI/bge-m3"

with timer("bs1"):
    response = client.embeddings.create(
        input=["查" * 1000] * 1,
        model=model
    )


