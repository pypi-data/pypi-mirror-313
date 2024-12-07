#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat_dev
# @Time         : 2024/7/8 21:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from openai import OpenAI
from meutils.pipe import *

# base_url = "https://openai-dev.chatfire.cn/audio/v1"


r = OpenAI(
    # base_url=base_url
).audio.speech.create(input="你好呀", model='tts-1', voice="alloy")

r.stream_to_file('xx.mp3')
