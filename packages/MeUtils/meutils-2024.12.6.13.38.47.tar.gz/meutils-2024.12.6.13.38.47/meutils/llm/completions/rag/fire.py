#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : moonshot
# @Time         : 2024/11/21 17:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 文件url 或者 文件id
import mimetypes

from meutils.pipe import *
from meutils.io.files_utils import to_bytes
from meutils.llm.openai_utils import to_openai_params

from openai import OpenAI, AsyncOpenAI
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, ChatCompletionRequest, CompletionUsage

moonshot_client = AsyncOpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"),
    base_url=os.getenv("MOONSHOT_BASE_URL")
)


# moonshot_client.files.

# len(moonshot_client.files.list().data)

class Completions(object):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    @staticmethod
    @alru_cache(ttl=15 * 60)
    async def file_extract(file):  # "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf"
        """todo 定时删除文件"""
        filename = Path(file).name
        mime_type, _ = mimetypes.guess_type(filename)  # mime_type = "application/octet-stream"
        file: bytes = await to_bytes(file)

        file_object = await moonshot_client.files.create(
            # file=file,
            # file=("filename.pdf", file),
            file=(filename, file, mime_type),
            purpose="file-extract"
        )
        logger.debug(file_object)

        response = await moonshot_client.files.content(file_id=file_object.id)
        return response.text

    async def create(self, request: ChatCompletionRequest):
        """[{'role': 'user', 'content': 'hi'}]
        {"type": "file_url", "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}}"""

        # logger.debug(request.urls)
        if request.urls:
            files = await asyncio.gather(*map(self.file_extract, request.urls))

            for file_content in files:
                request.system_messages.append({
                    "role": "system",
                    "content": file_content,
                })

            request.messages = request.system_messages + [{'role': 'user', 'content': request.last_content}]

        logger.debug(request)

        data = to_openai_params(request)
        return await AsyncOpenAI(api_key=self.api_key).chat.completions.create(**data)


# data: {"event": "message", "task_id": "900bbd43-dc0b-4383-a372-aa6e6c414227", "id": "663c5084-a254-4040-8ad3-51f2a3c1a77c", "answer": "Hi", "created_at": 1705398420}\n\n
if __name__ == '__main__':
    c = Completions()

    request = ChatCompletionRequest(
        model="qwen-turbo-2024-11-01",
        messages=[
            {
                'role': 'system',
                'content': '你是一个文件问答助手'
            },
            {
                'role': 'user',
                # 'content': {
                #     "type": "file_url",
                #     "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}
                # },
                'content': [
                    {
                        "type": "text",
                        "text": "这个文件讲了什么？"
                    },
                    # 多轮的时候要剔除
                    {
                        "type": "file_url",
                        "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}
                    }
                ]
            },
            # {'role': 'assistant', 'content': "好的"},
            # {
            #     'role': 'user',
            #     # 'content': {
            #     #     "type": "file_url",
            #     #     "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}
            #     # },
            #     'content': [
            #         {
            #             "type": "text",
            #             "text": "错了 继续回答"
            #         },
            #         # {
            #         #     "type": "file_url",
            #         #     "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}
            #         # }
            #     ]
            # }
        ]

    )

    arun(c.create(request))
