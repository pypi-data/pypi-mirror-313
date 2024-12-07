#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : xx
# @Time         : 2024/11/15 09:19
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

url = "https://chat.tune.app/_next/static/chunks/7116-1a0ed7d4153eddad.js"



s =  httpx.get(url).text.split(',A=(0,a.$)("')[1][:40]