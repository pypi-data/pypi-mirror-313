#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : feishu
# @Time         : 2021/1/20 6:04 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : todo: 输出json优化

from meutils.pipe import *

DEFAULT = "https://open.feishu.cn/open-apis/bot/v2/hook/f7cf6f2a-30da-4e7a-ae6f-b48c8bb1ecf8"
IMAGES = "https://open.feishu.cn/open-apis/bot/v2/hook/c903e9a7-ece0-4b98-b395-0e1f6a1fb31e"
VIDEOS = "https://open.feishu.cn/open-apis/bot/v2/hook/0f926e89-90de-4211-90c5-fd99e8db8ea3"
LLM = "https://open.feishu.cn/open-apis/bot/v2/hook/3c4f3756-c824-4942-9f8f-561a74e7c6e9"
LLM_REVERSE = "https://open.feishu.cn/open-apis/bot/v2/hook/cd5c9126-a882-4a24-9f1b-145cd1dcc769"

Vison = ""
# AUDIOS_TTS = "https://open.feishu.cn/open-apis/bot/v2/hook/ff7d4b86-d238-436c-9447-f88cf603454d"
AUDIO = "https://open.feishu.cn/open-apis/bot/v2/hook/80c2a700-adfa-4b9b-8e3f-00b78f2f5c8b"


@background_task
def send_message(
        content: Any = '',
        title: Optional[str] = '',
        message: Optional[Dict] = None,
        url: str = DEFAULT,
        n: int = 1,
):
    if any(i in str(content).lower() for i in {'重定向', 'pass'}):
        return

    if any((content, title)):

        if isinstance(content, str):  # todo: post_process
            content = content.replace("<", "【").replace(">", "】")
            contents = [content]
            # contents = [{"a": 1}]*3

        elif isinstance(content, (list,)):
            contents = list(map(bjson, content))

        elif isinstance(content, (dict,)):
            contents = [bjson(content)]

        elif isinstance(content, BaseModel):
            contents = [content.model_dump_json(indent=4)]

        else:
            contents = [str(content)]

        message = message or {
            "msg_type": "interactive",
            "card": {
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "content": str(content),
                            "tag": "lark_md"
                        }
                    } for content in contents
                ],
                "header": {
                    "title": {
                        "content": str(title).title(),
                        "tag": "plain_text"
                    }
                }
            }
        }
        r = None
        for i in range(n):
            time.sleep(i ** 2)
            r = httpx.post(url, json=message)
        return r and r.text


@decorator
def catch(
        fn: Callable,
        task_name: Optional[str] = None,
        trace: bool = True,
        url: Optional[str] = None,
        *args,
        **kwargs
):
    task_name = task_name or fn.__name__
    r = None
    try:
        # s = time.perf_counter()
        r = fn(*args, **kwargs)
        # content = f"Task done in {time.perf_counter() - s:.2f} s"

    except Exception as e:
        content = str(e)
        if trace:
            content = traceback.format_exc()
        send_message(title=task_name, content=content, url=url, n=3)

    return r


if __name__ == '__main__':
    send_message("xxx", title=None)

    # @catch(task_name='这是一个任务名')
    # def f():
    #     time.sleep(3)
    #     1 / 0
    #
    #
    # f()
    # with timer():
    #     send_message(BaseModel, title='GitHub Copilot Chat Error')

    # print(bjson(['a']))
