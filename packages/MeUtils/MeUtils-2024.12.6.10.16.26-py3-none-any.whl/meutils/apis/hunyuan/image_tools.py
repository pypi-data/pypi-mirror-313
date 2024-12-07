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
from meutils.decorators.retry import retrying, IgnoredRetryException
from meutils.schemas.yuanbao_types import FEISHU_URL, YUANBAO_BASE_URL
from meutils.schemas.image_types import HunyuanImageProcessRequest

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.io.files_utils import to_url
from meutils.notice.feishu import send_message


@retrying(min=3, ignored_exception_types=(IgnoredRetryException,))
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

        # 新版本的位置可能不一样 注意
        # data = json_repair.repair_json(
        #     response.text.replace(r'\u0026', '&').rsplit("data: [TRACEID", 1)[0],
        #     return_objects=True
        # )[-1]

        skip_strings = ['DONE', 'TRACEID']
        data = response.text.replace(r'\u0026', '&').splitlines() | xsse_parser(skip_strings=skip_strings)
        data = data and data[-1]
        logger.debug(data)

        # todo: 错误处理
        if isinstance(data, dict) and any(data["code"] == code for code in {"429"}):
            Exception(f"重试: {response.text}")

        elif isinstance(data, list) or any(i in response.text for i in {"当前图片没有检测到水印"}):  # 跳过重试并返回原始错误
            raise IgnoredRetryException(f"忽略重试: \n{response.text}")

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
        image = "https://oss.ffire.cc/files/kling_watermark.png"
        image = "https://cdn.meimeiqushuiyin.cn/2024-12-05/ori/tmp_0511a4cb2066ffc309fa6f7a733ac1e93236709bf46c9430.jpg"
        image = "https://cdn.meimeiqushuiyin.cn/2024-12-05/ori/tmp_de5e186878b079a87d22c561f17e6853.jpg"
        request = HunyuanImageProcessRequest(image=image, task='removewatermark')

        arun(image_process(request))
