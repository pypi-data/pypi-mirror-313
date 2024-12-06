#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : video_types
# @Time         : 2024/9/13 10:15
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


class VideoRequest(BaseModel):
    model: str = "cogvideox"
    prompt: str = "比得兔开小汽车，游走在马路上，脸上的表情充满开心喜悦。"
    image_url: Optional[str] = None

    class Config:
        frozen = True
