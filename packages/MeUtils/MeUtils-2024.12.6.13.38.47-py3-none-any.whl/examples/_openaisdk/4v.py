#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 4v
# @Time         : 2023/11/20 10:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os
#
from meutils.pipe import *
from meutils.io.image import image_to_base64
from openai import OpenAI, AsyncOpenAI
from openai.types.chat.completion_create_params import ResponseFormat
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest

base_url = os.getenv('OPENAI_BASE_URL')
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY_OPENAI"))
# openai = OpenAI(api_key=os.getenv("SILICONFLOW_API_KEY"), base_url=os.getenv("SILICONFLOW_BASE_URL"))
# openai = OpenAI(
#     # api_key=os.getenv("TOGETHER_API_KEY"),
#     # base_url=os.getenv("TOGETHER_BASE_URL")
# )

# openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY_GUOCHAN"))

# openai = OpenAI(api_key=os.getenv("ZHIPUAI_API_KEY"), base_url=os.getenv("ZHIPUAI_BASE_URL"))

# image_url = image_to_base64('/Users/betterme/PycharmProjects/AI/ChatLLM/data/invoice.jpg', for_image_url=True)
image_url1 = image_to_base64('1.png', for_image_url=True)
base64_image = image_to_base64('1.png', for_image_url=True)

# file_to_base64("/Users/betterme/PycharmProjects/AI/ChatLLM/examples/openaisdk/new.pdf")
# print(image_url2)

image_url1 = "https://img-home.csdnimg.cn/images/20201124032511.png"
image_url2 = "https://taosha01-1253585015.cos.ap-shanghai.myqcloud.com/typora/24951712814992_.pic_thumbnail.jpg"

image_urls = [
    {"type": "image_url", "image_url": {"url": image_to_base64(p, for_image_url=True)}}
    for p in Path().glob('img_7.png')
]
#
messages = [
    # {"role": "system", "content": "你是位数学专家，擅长解决复杂的数学问题。"},
    # {"role": "system", "content": '你是一个AI助手，将用JSON格式返回.'},
    {
        "role": "user",
        "content": [
            {"type": "text",
             # "text": f"解释 {base64_image}"
             "text":
                 """
                 解释下
                 """
             },
            # {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            {"type": "image_url", "image_url": {"url": base64_image}},

            # {"type": "image_url", "image_url": {"url": image_url1}},
            # {"type": "image_url", "image_url": {"url": image_url2}},

            # {"type": "video_url", "video_url": "https://oss.ffire.cc/files/douyin.mp4"},

            # *image_urls

        ],

    }
]
response = openai.chat.completions.create(
    # model='gpt-4-vision-preview',
    model='gpt-4o',

    # model="gemini-pro-vision",
    # model='gemini-1.5-flash-latest',

    # model="claude-3-haiku-20240307",
    # model="claude-3-sonnet-20240229",
    # model="claude-3-opus-20240229",

    # model='glm-4v',
    # model='glm-4v-plus',

    # model='step-1v',
    # model='yi-vision',

    # model="Pro/OpenGVLab/InternVL2-8B",
    # model="meta-llama/Llama-Vision-Free",
    # model="grok-vision-beta",

    # model='kimi', # ocr

    messages=messages,
    max_tokens=100,
    temperature=0,
    # response_format={"type": "json_object"}
)

print(response.dict())


# response = client.chat.completions.create(input='你好', model='tts-1', voice='alloy')
