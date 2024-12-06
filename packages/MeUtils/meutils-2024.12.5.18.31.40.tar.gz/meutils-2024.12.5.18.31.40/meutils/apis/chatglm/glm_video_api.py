#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : video
# @Time         : 2024/7/26 12:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling

from meutils.schemas.video_types import VideoRequest

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)

from zhipuai import ZhipuAI
from zhipuai.types.video import VideoObject, VideoResult

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=5i64gO"


@retrying(max_retries=3, predicate=lambda r: r.task_status is None)
async def create_task(request: VideoRequest, api_key: Optional[str] = None):
    api_key = api_key or await get_next_token_for_polling(FEISHU_URL, from_redis=True)

    client = ZhipuAI(api_key=api_key)  # 请填写您自己的APIKey
    response = client.videos.generations(
        model=request.model,
        prompt=request.prompt,
        extra_body={
            "image_url": request.image_url
        }
    )

    response = VideoObject.construct(**response.model_dump(), system_fingerprint=api_key)
    response.id = f"cogvideox-{response.id}"
    # response
    logger.debug(response)
    logger.debug(response.task_status)

    # response
    return response


async def get_task(task_id, api_key):
    task_id = isinstance(task_id, str) and task_id.split("-", maxsplit=1)[-1]

    client = ZhipuAI(api_key=api_key)  # 请填写您自己的APIKey

    response = client.videos.retrieve_videos_result(
        id=task_id
    )
    return response

# {
#     "model": "cogvideox",
#     "request_id": "8868902201637896192",
#     "task_status": "SUCCESS",
#     "video_result": [
#         {
#             "cover_image_url": "https://sfile.chatglm.cn/testpath/video_cover/4d3c5aad-8c94-5549-93b7-97af6bd353c6_cover_0.png",
#             "url": "https://sfile.chatglm.cn/testpath/video/4d3c5aad-8c94-5549-93b7-97af6bd353c6_0.mp4"
#         }
#     ]
# }
# }

# VideoResult
# VideoObject(id='340817255120805129017958079360725371', model='cogvideox', video_result=None, task_status='PROCESSING', request_id='9017958079360725355', system_fingerprint='cf36b5587554cc3d34abd59ce252b19b.zzJ4co4kNEWPSbnm')

# VideoResult
if __name__ == '__main__':
    # r = arun(create_task(VideoRequest()))
    pass
