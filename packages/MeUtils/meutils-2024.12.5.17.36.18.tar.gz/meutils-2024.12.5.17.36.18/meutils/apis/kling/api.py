#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : api
# @Time         : 2024/10/10 10:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/nodetool-ai/nodetool/blob/bfd32cf40dcf1fe2711803f9c8730c0e816067e4/src/nodetool/nodes/kling/api.py#L99

import jwt

from meutils.pipe import *
from meutils.config_utils.lark_utils import get_next_token_for_polling

from meutils.schemas.kling_types import API_BASE_URL, API_FEISHU_URL, STATUSES, send_message
from meutils.schemas.kling_types import ImageRequest, VideoRequest


def encode_jwt_token(ak, sk):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,  # 有效时间，此处示例代表当前时间+1800s(30min)
        "nbf": int(time.time()) - 5  # 开始生效的时间，此处示例代表当前时间-5秒
    }
    token = jwt.encode(payload, sk, headers=headers)
    logger.debug(token)
    return token


async def create_task(request: VideoRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(API_FEISHU_URL)
    token = "ee6503baf0e447d59a3812fb2a344570|da8322347a7b4d5a9c04a088427883f7"
    ak, sk = token.split("|")

    headers = {
        'content-type': 'application/json;charset=utf-8',
        "Authorization": f"Bearer {encode_jwt_token(ak, sk)}"
    }
    payload = request.model_dump(exclude_none=True)
    async with httpx.AsyncClient(base_url=API_BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/v1/videos/text2video", json=payload)
        response.raise_for_status()
        return response.json()
        #
        # if response.is_success:
        #     data = response.json()
        #     return data
        # else:
        #     raise Exception(f"请求失败，状态码：{response.status_code}，响应内容：{response.text}")


if __name__ == '__main__':
    # api_token = encode_jwt_token(ak, sk)
    # print(api_token)  # 打印生成的API_TOKEN
    arun(create_task(VideoRequest(prompt="可爱的小姐姐")))
