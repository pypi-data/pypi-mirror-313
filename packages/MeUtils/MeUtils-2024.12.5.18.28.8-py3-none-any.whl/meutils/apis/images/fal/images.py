#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/11/13 15:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra/api

from meutils.pipe import *
from meutils.schemas.image_types import ImageRequest, FluxImageRequest, SDImageRequest, ImagesResponse
from meutils.schemas.fal_types import FEISHU_URL
from meutils.config_utils.lark_utils import get_next_token_for_polling

from fal_client import AsyncClient, SyncClient

DEFAULT_MODEL = "fal-ai/flux-pro/v1.1-ultra"
MODELS = {
    "flux-1.1-pro-ultra": "fal-ai/flux-pro/v1.1-ultra",
    "fal-ai/recraft-v3": "fal-ai/recraft-v3"
}


async def generate(request: ImageRequest, token: Optional[str] = None):
    """https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra/api#api-call-submit-request
    """
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)
    request.model = MODELS.get(request.model, DEFAULT_MODEL)
    logger.debug(request)

    data = await AsyncClient(key=token).run(
        application=request.model,
        arguments={
            "prompt": request.prompt,
            "seed": request.seed,
            "num_images": request.n,

            "aspect_ratio": "16:9", # 21:9, 16:9, 4:3, 1:1, 3:4, 9:16, 9:21 ImageSize

            "enable_safety_checker": False,
            "safety_tolerance": "6",
            "output_format": "png",
        }
    )

    return ImagesResponse(data=data.get("images", data))

if __name__ == '__main__':
    pass
    request = ImageRequest(prompt='a dog')
    arun(generate(request))
