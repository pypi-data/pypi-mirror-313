#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : image
# @Time         : 2024/10/11 15:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json_repair

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.schemas.yuanbao_types import FEISHU_URL, YUANBAO_BASE_URL
from meutils.schemas.image_types import HunyuanImageProcessRequest

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.io.files_utils import to_url


@retrying(min=3)
async def image_process(request: HunyuanImageProcessRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)

    payload = {
        "imageUrl": request.image if request.image.startswith('http') else await to_url(request.image),
    }
    if request.task == 'style':
        payload.update({
            "style": request.style,
            "prompt": f"转换为{request.style}",
        })

    headers = {
        'cookie': token
    }
    async with httpx.AsyncClient(base_url=YUANBAO_BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post(f"/api/image/{request.task}", json=payload)
        response.raise_for_status()
        logger.debug(response.text)

        data: dict = json_repair.repair_json(response.text.replace(r'\u0026', '&'), return_objects=True)[-2]
        if any(data["code"] == code for code in {"429"}):
            Exception("重试")

        data = {
            "data": [
                {
                    "url": data["imageUrl"],
                    "imageUrl": data["imageUrl"],
                    "thumbnailUrl": data["thumbnailUrl"],
                }
            ]
        }

        return data


if __name__ == '__main__':
    # request = ImageProcessRequest(image="https://oss.ffire.cc/files/kling_watermark.png", task='removewatermark')

    with timer():
        image = "https://sfile.chatglm.cn/chatglm4/3dcb1cc2-22ad-420b-9d16-dc71dffc02b2.png"
        request = ImageProcessRequest(image=image, task='clarity')

        arun(image_process(request))
