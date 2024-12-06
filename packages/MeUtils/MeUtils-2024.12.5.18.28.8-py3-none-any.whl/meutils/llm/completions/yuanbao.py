#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : yuanbao
# @Time         : 2024/6/11 18:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import asyncio

from aiostream import stream

from meutils.pipe import *
from meutils.io.image import image2nowatermark_image

from meutils.llm.utils import oneturn2multiturn
from meutils.schemas.openai_types import ChatCompletionRequest
from meutils.schemas.image_types import HunyuanImageRequest

from meutils.schemas.yuanbao_types import FEISHU_URL, SSEData, YUANBAO_BASE_URL, API_CHAT, API_GENERATE_ID, \
    API_DELETE_CONV, \
    GET_AGENT_CHAT
from meutils.config_utils.lark_utils import get_next_token_for_polling, aget_spreadsheet_values


# import rev_HunYuan


class Completions(object):

    @classmethod
    async def generate(cls, request: HunyuanImageRequest):
        response = cls().create(image_request=request)
        urls = await stream.list(response)
        urls = await asyncio.gather(*map(image2nowatermark_image, urls))

        return {
            "data": [{"url": url} for url in urls]
        }

    async def create(
            self,
            request: Optional[ChatCompletionRequest] = None,
            image_request: Optional[HunyuanImageRequest] = None,
            token: Optional[str] = None
    ):
        token = token or await get_next_token_for_polling(FEISHU_URL, check_token=check_token)

        logger.debug(token)

        prompt = request and oneturn2multiturn(request.messages) or image_request.prompt

        payload = {
            "model": "gpt_175B_0404",
            "version": "v2",
            "supportHint": 2,

            "prompt": prompt,
            # "displayPrompt": "画条可爱的狗狗",
            # "displayPromptType": 1,
            "multimedia": [],
            # "agentId": "gtcnTp5C1G",

            "plugin": "Adaptive",

            "options": {
                "imageIntention": {
                    "needIntentionModel": True,
                    "backendUpdateFlag": 2,
                    "intentionStatus": True,
                    "userIntention": {
                        "resolution": "1280x1280",
                    }
                }
            },

        }
        if image_request:
            payload["displayImageIntentionLabels"] = [
                {"type": "resolution", "disPlayValue": "超清", "startIndex": 0, "endIndex": 1}
            ]
            payload["options"]["imageIntention"]["userIntention"].update(
                {
                    "style": image_request.style,

                    "scale": image_request.size,

                    # todo: 默认四张 不生效
                    # "N": image_request.n,
                    # "num": image_request.n,
                    # "Count": image_request.n,

                }
            )

        headers = {
            'cookie': token
        }
        async with httpx.AsyncClient(base_url=YUANBAO_BASE_URL, headers=headers, timeout=300) as client:
            # chatid = (await client.post(API_GENERATE_ID)).text
            chatid = uuid.uuid4()

            async with client.stream(method="POST", url=f"{API_CHAT}/{chatid}", json=payload) as response:
                logger.debug(response.status_code)
                response.raise_for_status()

                async for chunk in response.aiter_lines():
                    sse = SSEData(chunk=chunk)
                    if image_request and sse.image:
                        logger.debug(sse.image)
                        yield sse.image

                    if request:
                        yield sse.content

    def generate_id(self, random: bool = True):
        if random:
            return f'{uuid.uuid4()}'
        return httpx.post(API_GENERATE_ID).text

    def delete_conv(self, chatid):
        response = httpx.post(f"{API_DELETE_CONV}/{chatid}")
        return response.status_code == 200


async def check_token(token):
    headers = {
        "cookie": token
    }
    try:
        async with httpx.AsyncClient(base_url=YUANBAO_BASE_URL, headers=headers, timeout=10) as client:
            response = await client.get("/api/info/general")
            response.raise_for_status()
            logger.debug(response.status_code)
            return True
    except Exception as e:
        logger.error(e)
        return False


if __name__ == '__main__':
    # chatid = generate_id()
    # print(chatid)
    # print(delete_conv(chatid))
    # payload = {
    #     # "model": "gpt_175B_0404",
    #     # "prompt": "1+1",
    #     "prompt": "错了",
    #
    #     # "plugin": "Adaptive",
    #     # "displayPrompt": "1+1",
    #     # "displayPromptType": 1,
    #     # "options": {},
    #     # "multimedia": [],
    #     # "agentId": "naQivTmsDa",
    #     # "version": "v2"
    # }
    # chat(payload)

    # async2sync_generator(Completions(api_key).achat('画条狗')) | xprint
    request = HunyuanImageRequest(prompt='画条狗', size='16:9')

    # arun(Completions().create(
    #     ChatCompletionRequest(messages=[{'role': 'user', 'content': '南京天气如何'}]),
    #     # image_request=request,
    #     # token=token
    # ))
    arun(Completions.generate(request))

    # df = arun(aget_spreadsheet_values(feishu_url=FEISHU__URL, to_dataframe=True))
    #
    # for i in df[0]:
    #     if not arun(check_token(i)):
    #         print(i)
    #
