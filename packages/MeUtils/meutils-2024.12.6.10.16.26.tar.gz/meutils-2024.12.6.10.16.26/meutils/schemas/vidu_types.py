#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : vidu_types
# @Time         : 2024/7/31 08:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://api.vidu.studio/vidu/v1"
UPLOAD_BASE_URL = "https://api.vidu.studio/tools/v1"  # /files/uploads

EXAMPLES = [
    {
        "input": {
            "prompts": [
                {
                    "type": "text",
                    "content": "两个人举起茶杯小口抿了一口。左边的人轻抿双唇后微笑，右边的人专注于他们的茶，形成一种静雅和微妙互动的场景。布景精致，淡雅的颜色、花卉布置和古典家具增强了优雅氛围。",
                }
            ],
            "enhance": True,
        },
        "type": "text2video",
        "settings": {
            "style": "general",
            "duration": 4,
            "model": "vidu-1",
            "aspect_ratio": "16:9",

        }
    },
    {
        "input": {
            "prompts": [
                {
                    "type": "text",
                    "content": "开花吧",
                    "enhance": True
                },
                {
                    "type": "image",
                    "content": "ssupload:?id=2368323193735387",
                    "enhance": True
                }
            ]
        },
        "type": "img2video",
        "settings": {
            "style": "general",
            "aspect_ratio": "16:9",
            "duration": 4,
            "model": "vidu-1"
        }
    }
]


class ViduRequest(BaseModel):
    model: str = "vidu-1"  # vidu-1.5

    prompt: Optional[str] = None
    url: Optional[str] = None  # ssupload:?id=
    style: str = "general"  # anime
    aspect_ratio: str = "16:9"
    duration: int = 4

    type: Optional[str] = None  # text2video img2video character2video

    payload: dict = {}

    def __init__(self, **data):
        super().__init__(**data)

        if self.duration > 4:
            self.duration = 8
        else:
            self.duration = 4

        input = {
            "prompts": [],
            "enhance": True
        }

        if self.prompt:
            input['prompts'].append(
                {
                    "type": "text",
                    "content": self.prompt,
                }
            )
        type = "text2video"
        if self.url:
            input['prompts'].append(
                {
                    "type": "image",
                    "content": self.url,
                    # "content": "ssupload:?id=2467831038260968",
                    # "src_img": "ssupload:?id=2467831032322652"
                }
            )
            type = "img2video"  # character2video

        self.payload = {
            "input": input,
            "type": self.type or type,
            "settings": {
                "style": self.style,
                "aspect_ratio": self.aspect_ratio,
                "duration": self.duration,
                "model": "vidu-1"  # vidu-high-performance
            }
        }

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "prompt": "一只可爱的黑白边境牧羊犬，头伸出车窗，毛发被风吹动，微笑着伸出舌头。",
                }
            ]
        }


class ViduUpscaleRequest(BaseModel):
    task_id: str  # vip
    creation_id: str


# todo: 兼容官方api https://kimi.moonshot.cn/chat/cs33f8j1ch3mt3umbsp0
text2video = {
    "type": "text2video",  # type (string, enum: text2video, img2video, character2video, upscale):
    "model": "vidu-1",
    "style": "general",

    "input": {
        "seed": 123,
        "enhance": True,
        "prompts": [
            {
                "type": "text",
                "content": "小白兔白又白"
            }
        ]
    },

    "output_params": {
        "sample_count": 1,
        "duration": 4
    },
    "moderation": False
}

img2video = {
    "type": "img2video",
    "model": "vidu-1",
    "style": "general",

    "input": {
        "enhance": True,
        "prompts": [
            {
                "type": "text",
                "content": "小白兔白又白"
            },
            {
                "type": "image",
                "content": "https://pic.netbian.com/uploads/allimg/170624/1722311498296151ea67.jpg"
            }
        ]
    },

    "output_params": {
        "sample_count": 1,
        "duration": 4
    },
    "moderation": False
}
