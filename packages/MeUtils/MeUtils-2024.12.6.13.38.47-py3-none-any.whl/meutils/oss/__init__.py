#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2024/3/14 17:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def upload(file: bytes, purpos="zhipu"):
    from meutils.oss.minio_oss import Minio
    from meutils.apis.chatglm.glm_video import upload_task

    file_task = upload_task(file)


