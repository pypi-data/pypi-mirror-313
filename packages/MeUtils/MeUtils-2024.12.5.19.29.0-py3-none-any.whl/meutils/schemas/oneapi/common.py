#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : oneapi_types
# @Time         : 2024/6/28 10:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.data.oneapi import NOTICE, FOOTER

BASE_URL = "https://api.chatfire.cn"
# BASE_URL = "https://api-dev.chatfire.cn"
FREE = 0.001

MODEL_PRICE = {
    # chatfire
    "ppu-0001": 0.0001,
    "ppu-001": 0.001,
    "ppu-01": 0.01,
    "ppu-1": 0.1,
    "api-oss": 0.01,
    "chatfire-translator": 0.01,
    "chatfire-all": 0.0001,
    "chatfire-law": 0.01,

    # 虚拟换衣fish
    "api-kolors-virtual-try-on": 0.1,
    "official-api-kolors-virtual-try-on": 0.8,

    # 语音克隆
    "official-api-fish-model": 0.1,
    "official-api-fish-tts": 0.01,

    # 官方api
    "official-api-cogvideox": 0.5,
    "official-api-kling-image": 0.02,
    "official-api-kling-video": 0.5,

    "official-api-vidu": 0.5,

    "official-api-hailuo-video": 0.3,
    "api-hailuo-video": 0.3,

    # delle3
    "api-images-kling": 0.04,
    "api-images-hunyuan": 0.04,
    "api-images-cogview-3": 0.01,
    "api-images-stable-diffusion": 0.01,

    "api-images-flux1.0-turbo": 0.02,
    "api-images-flux-schnell": 0.01,
    "api-images-flux1.0-schnell": 0.01,
    "api-images-flux1.0-dev": 0.05,
    "api-images-flux1.0-pro": 0.1,
    "api-images-flux1.1-pro": 0.1,
    "api-images-recraftv3": 0.03,

    "api-tripo3d": 0.1,

    # 图片 音频 视频
    "recraftv3": 0.03,
    "recraftv3-halloween": 0.03,
    "chat-recraftv3": 0.03,
    "chat-recraftv3-halloween": 0.03,

    "api-asr": 0.01,
    "api-stt": 0.01,
    "api-tts": 0.01,

    "step-1x-medium": 0.1,

    "kolors": 0.02,
    "kling": 0.02,

    "ideogram": 0.3,

    # replicate
    "api-replicate-flux-1.1-pro": 0.040,
    "api-replicate-flux-1.1-pro-ultra": 0.060,
    "api-replicate-flux-dev": 0.025,
    "api-replicate-flux-pro": 0.055,
    "api-replicate-flux-schnell": 0.003,
    "api-replicate-ideogram-v2": 0.080,
    "api-replicate-ideogram-v2-turbo": 0.050,
    "api-replicate-recraft-v3": 0.040,
    "api-replicate-recraft-v3-svg": 0.080,
    "api-replicate-stable-diffusion-3": 0.035,
    "api-replicate-stable-diffusion-3.5-large": 0.065,
    "api-replicate-stable-diffusion-3.5-large-turbo": 0.040,
    "api-replicate-stable-diffusion-3.5-medium": 0.035,

    "flux": 0.01,
    "flux-schnell": 0.01,
    "flux-dev": 0.03,
    "flux-pro": 0.05,
    "flux-pro-max": 0.1,
    "flux.1.1-pro": 0.1,
    "black-forest-labs/flux.1.1-pro": 0.1,

    "stable-diffusion-3-5-large": 0.0001,
    "chat-stable-diffusion-3-5-large": 0.1,

    "chat-step-1x-medium": 0.1 / 4,

    "chat-flux-schnell": 0.01,
    "chat-flux-dev": 0.03,
    "chat-flux-pro": 0.05,
    "chat-flux-pro-max": 0.1,
    "chat-ideogram": 0.3,

    "chat-kolors": 0.02,
    "chat-kling": 0.02,
    "chat-video": 0.1,
    "chat-video-kling": 0.1,
    "chat-video-gen3": 0.1,
    "chat-video-vidu": 0.1,
    "chat-video-vidu-vip": 0.3,
    "chat-flux.1.1-pro": 0.1,

    # aitools
    "api-aitools": 0.007,

    # 文档智能
    "api-textin": 0.02,
    "api-pdf-to-markdown": 0.02,
    "api-file-to-text": 0.02,
    "api-ocr": 0.01,
    "api-ocr-pro": 0.02,

    # api
    "api-watermark-remove": 0.007,
    "api-idphotos": 0.01,
    "api-pcedit": 0.007,
    "api-faceswap": 0.01,

    "api-kling": 0.1,
    "api-kling-vip": 0.5,

    "api-vidu": 0.09,
    "api-vidu-vip": 0.3,

    "api-cogvideox": 0.1,
    "api-cogvideox-vip": 0.4,

    "api-runwayml-gen3": 0.1,

    "api-translator": 0.0001,
    "api-voice-clone": 0.01,

    "api-sunoai-chirp": 0.1,
    "api-sunoai-audio": 0.01,  # file
    "api-sunoai-lyrics": 0.01,
    "api-sunoai-cover": 0.01,
    "api-sunoai-stems": 0.01,

    "suno-v3": 0.1,
    "suno-v3.5": 0.1,
    "suno-chat": 0.1,
    "chirp-v3": 0.1,
    "chirp-v3.5": 0.1,

    "api-reranker": 0.01,

    # all
    # "o1-mini": 0.2,
    # "o1-preview": 0.4,
    # "o1-mini": 0.1,
    # "o1-preview": 0.2,
    # "o1-mini-2024-09-12": 0.1,
    # "o1-preview-2024-09-12": 0.2,
    "o1-mini-all": 0.2,
    "o1-preview-all": 0.4,
    "gpt-4-all": 0.1,
    "gpt-4o-all": 0.1,

    "gpt-4-gizmo-*": 0.1,
    "advanced-voice": 1,

    "claude-3-5-sonnet-all": 0.2,

    # 前置联网
    "net-gpt-3.5-turbo": 0.01,
    "net-gpt": 0.01,
    "net-gpt-4": 0.1,
    "perplexity": 0.01,
    "net-claude": 0.015,

    # 逆向
    "cogview-3": 0.01,
    "cogview-3-plus": 0.02,

    "glm-4-all": 0.01,
    "kimi-all": 0.01,

    "spark-all": 0.01,
    "step-1-all": 0.01,
    "step-all": 0.01,
    "hunyuan-all": 0.01,

    "chat-stable-diffusion-3": 0.02,

    # 搜索
    "api-search": 0.01,

    # "ai-search": 0.05,
    "ai-search-pro": 0.1,
    # "ai-search:scholar": 0.05,
    "ai-search-pro:scholar": 0.1,

    "ai-search": FREE,
    "ai-search:scholar": FREE,

    "midjourney": 0.14,  # chat

    "mj_imagine": 0.1 * 0.6,
    "mj_variation": 0.1 * 0.6,
    "mj_high_variation": 0.1 * 0.6,
    "mj_low_variation": 0.1 * 0.6,
    "mj_pan": 0.1 * 0.6,
    "mj_blend": 0.1 * 0.6,
    "mj_inpaint": 0,
    "mj_reroll": 0.1 * 0.6,

    "mj_upscale": 0.05 * 0.6,
    "mj_custom_zoom": 0,
    "mj_describe": 0.05 * 0.6,
    "mj_modal": 0.1 * 0.6,
    "mj_shorten": 0.1 * 0.6,
    "mj_zoom": 0.1 * 0.6,
    "swap_face": 0.05 * 0.6,

}

MODEL_RATIO = {
    # 智能体
    "gpt-4-plus": 2.5,
    "gpt-4o-plus": 2.5,

    # embedding & rerank
    "rerank-multilingual-v2.0": 0.1,
    "rerank-multilingual-v3.0": 0.1,
    "BAAI/bge-reranker-v2-m3": 0.1,
    "jina-reranker-v2-base-multilingual": 0.1,
    "netease-youdao/bce-reranker-base_v1": 0.1,
    "BAAI/bge-m3": 0.1,
    "bge-m3": 0.1,

    "bge-large-zh-v1.5": 0.1,
    "BAAI/bge-large-zh-v1.5": 0.1,
    "bge-large-en-v1.5": 0.1,
    "BAAI/bge-large-en-v1.5": 0.1,

    "text-embedding-3-large": 0.5,
    "text-embedding-3-small": 0.5,
    "text-embedding-ada-002": 0.5,

    # 百川
    'baichuan4-turbo': 7.5,
    'baichuan4-air': 0.49,
    'baichuan4': 50,
    'baichuan3-turbo': 6,
    'baichuan3-turbo-128k': 12,
    'baichuan2-turbo': 4,

    "claude-3-5-haiku-20241022": 4,
    "anthropic/claude-3-5-haiku-20241022:beta": 4,

    "grok": 2.5,
    "grok-beta": 2.5,
    # "grok2": 1,
    # "grok-2": 1,
    "x-ai/grok-beta": 2.5,
    "grok-vision-beta": 2.5,

    # 定制
    "lingxi-all": 1,

    "kimi": 5,
    "kimi-128k": 5,

    # 智谱
    'glm-4-9b-chat': 0.05,  # 特价
    "glm-3-turbo": 0.05,  # 特价
    "glm-4-flash": 0.05,  # 特价
    "glm-4-air": 0.05,  # 特价

    "glm-4": 2.5,
    "glm-4-0520": 2.5,
    "glm-4-airx": 10,
    "glm-4v": 2.5,
    "glm-4v-plus": 1,  # 2.5

    # 月之暗面 https://platform.moonshot.cn/docs/price/chat#%E4%BA%A7%E5%93%81%E5%AE%9A%E4%BB%B7
    "moonshot-v1-8k": 6 / 2,  # 特价
    "moonshot-v1-32k": 12 / 2,  # 特价
    "moonshot-v1-128k": 60 / 2,  # 特价

    # 阿里千问 https://dashscope.console.aliyun.com/billing
    "qwen-long": 0.25,
    "qwen-turbo": 1,
    "qwen-plus": 2,
    "qwen-max": 20,
    "qwen-max-longcontext": 20,
    "qwen-turbo-2024-11-01": 0.15,

    "qwen2.5-coder-7b-instruct": 0.05,
    "qwen2.5-7b-instruct": 0.05,
    "qwen2.5-14b-instruct": 0.7 / 2,
    "qwen2.5-32b-instruct": 1.26 / 2,
    "qwen2.5-72b-instruct": 4.13 / 2,
    "qwen2.5-math-72b-instruct": 4.13 / 2,
    "qwen2.5-coder-32b-instruct": 0.5,
    "qwen/qwq-32b-preview": 1,
    "Qwen/QwQ-32B-Preview": 1,

    "qwen1.5-7b-chat": 0.05,  # 特价
    "qwen1.5-14b-chat": 0.7,
    "qwen1.5-32b-chat": 1.75,
    "qwen1.5-110b-chat": 3.5,

    "qwen2-1.5b-instruct": 0.05,  # 特价
    "qwen2-7b-instruct": 0.05,  # 特价
    "qwen2-57b-a14b-instruct": 1.26,
    "qwen2-72b-instruct": 4.13,
    "farui-plus": 10,  # 法律大模型
    'qwen2-math-72b-instruct': 4.13,

    # 讯飞 https://xinghuo.xfyun.cn/sparkapi?scr=price
    'spark-lite': 0.05,  # 特价
    'spark-pro': 15 / 5,  # 特价
    'spark-max': 15,
    'spark-ultra': 50,

    # 阶跃星辰 https://platform.stepfun.com/docs/pricing/details
    "step-1-8k": 2.5,
    "step-1-32k": 7.5,
    "step-1v-8k": 2.5,
    "step-1v-32k": 7.5,

    # 零一万物 https://platform.lingyiwanwu.com/docs#%E8%AE%A1%E8%B4%B9%E5%8D%95%E5%85%83
    "yi-spark": 0.05,  # 特价
    "yi-1.5-6b-chat": 0.05,  # 特价
    "yi-1.5-9b-chat-16k": 0.05,  # 特价
    "yi-34b-chat": 0.63,
    "yi-34b-chat-0205": 0.63,
    "yi-1.5-34b-chat-16k": 0.63,

    "yi-lightning": 0.5,
    "yi-large": 10,
    "yi-large-turbo": 6,
    "yi-large-rag": 12.5,
    "yi-medium": 1.25,
    "yi-medium-200k": 6,
    "yi-vision": 3,

    # minimax https://platform.minimaxi.com/document/price?id=6433f32294878d408fc8293e
    "abab6.5-chat": 15 / 7.5,
    "abab6.5s-chat": 5,
    "abab6.5t-chat": 2.5,
    "abab6.5g-chat": 2.5,
    "abab5.5-chat": 7.5,
    "abab5.5s-chat": 2.5,

    # deepseek
    "deepseek-chat": 0.5,
    "deepseek-coder": 0.5,
    'deepseek-coder-v2-instruct': 0.5,
    'deepseek-v2-chat': 0.5,
    'deepseek-llm-67b-chat': 0.5,

    # 豆包
    "doubao-lite-128k": 0.4,
    "doubao-lite-32k": 0.15,
    "doubao-lite-4k": 0.15,
    "doubao-pro-128k": 2.5,
    "doubao-pro-32k": 0.4,
    "doubao-pro-4k": 0.4,

    # 商汤 https://platform.sensenova.cn/pricing
    # https://platform.sensenova.cn/doc?path=/pricingdoc/pricing.md
    "SenseChat-Turbo": 1 / 5,  # 特价
    "SenseChat": 6 / 5,  # 特价
    "SenseChat-32K": 18 / 5,  # 特价
    "SenseChat-128K": 30 / 5,  # 特价
    "SenseChat-5": 20 / 5,  # 最新版本#  特价
    "SenseChat-Vision": 50 / 5,  # 图生文#  特价
    "SenseChat-5-Cantonese": 13.5 / 5,  # 粤语大模型#  特价

    # 腾讯混元
    "hunyuan": 7.143,
    "hunyuan-lite": 4,
    "hunyuan-pro": 50,
    "hunyuan-standard": 5,
    "hunyuan-standard-256k": 60,

    # 百度文心
    "ERNIE-Speed-8K": 0.2858,
    "ERNIE-Speed-128K": 0.2858,

    "ERNIE-3.5-8K": 2,
    "ERNIE-3.5-128K": 4,

    "ERNIE-4.0-Turbo-8K": 15,
    "ERNIE-4.0-8K": 20,

    "text-ada-001": 0.2,
    "text-babbage-001": 0.25,
    "text-davinci-edit-001": 10,

    "text-moderation-latest": 0.1,
    "text-moderation-stable": 0.1,
    "tts-1": 7.5,
    "tts-1-1106": 7.5,
    "tts-1-hd": 15,
    "tts-1-hd-1106": 15,
    "whisper-1": 15,

    "claude-3-haiku-20240307": 0.125,
    "claude-3-sonnet-20240229": 1.5,

    "claude-3-opus-20240229": 7.5,
    "anthropic/claude-3-opus:beta": 7.5,  # openrouter

    "claude-3-5-sonnet-20240620": 1.5,
    "claude-3-5-sonnet-20241022": 1.5,

    "anthropic/claude-3.5-sonnet": 1.5,
    "anthropic/claude-3.5-sonnet:beta": 4,  # 1022

    "command": 0.5 * 2,
    "command-light": 0.5 * 2,
    "command-light-nightly": 0.5 * 2,
    "command-nightly": 0.5 * 2,
    "command-r": 0.25 * 2,
    "command-r-plus": 1.5 * 2,

    "command-r-08-2024": 0.075 * 2,
    "command-r-plus-08-2024": 1.25 * 2,

    "dall-e-3": 16,

    "gemini-1.0-pro-001": 1,
    "gemini-1.0-pro-latest": 1,
    "gemini-1.0-pro-vision-001": 1,
    "gemini-1.0-pro-vision-latest": 1,

    "gemini-1.5-flash-002": 0.3,  # 重定向到openrouter
    "google/gemini-flash-1.5-8b": 0.3,  # openrouter  $0.0375 $0.15

    "gemini-1.5-flash-latest": 0.1,
    "gemini-1.5-flash-exp-0827": 0.1,
    "google/gemini-flash-1.5-exp": 0.1,  # openrouter免费
    "google/gemini-flash-1.5-8b-exp": 0.1,  # openrouter免费

    "gemini-1.5-pro-001": 1,
    "gemini-1.5-pro-002": 1,
    "gemini-1.5-pro-latest": 1.75,
    "gemini-1.5-pro-exp-0827": 1.75,
    "google/gemini-pro-1.5-exp": 1,  # openrouter免费

    "gemini-1.5-pro": 2,
    "gemini-pro": 1,
    "gemini-pro-vision": 1,
    "gemini-ultra": 1,

    "gpt-3.5-turbo": 0.75,
    "gpt-3.5-turbo-0125": 0.25,
    "gpt-3.5-turbo-0613": 0.75,
    "gpt-3.5-turbo-1106": 0.5,
    "gpt-3.5-turbo-16k": 1.5,
    "gpt-3.5-turbo-16k-0613": 1.5,
    "gpt-3.5-turbo-instruct": 0.75,
    "gpt-4": 15,
    "gpt-4-0125-preview": 5,
    "gpt-4-0613": 15,
    "gpt-4-1106-preview": 5,
    "gpt-4-1106-vision-preview": 5,
    "gpt-4-32k": 30,
    "gpt-4-32k-0613": 30,
    "gpt-4-all": 15,
    "gpt-4-gizmo-*": 15,
    "gpt-4-turbo": 5,
    "gpt-4-turbo-2024-04-09": 5,
    "gpt-4-turbo-preview": 5,
    "gpt-4-vision-preview": 5,
    "chatgpt-4o-latest": 2.5,
    "gpt-4o-realtime-preview": 2.5,
    "gpt-4o-realtime-preview-2024-10-01": 2.5,

    "gpt-4o": 2.5,
    "gpt-4o-all": 2.5,  # 逆向
    "gpt-4o-2024-05-13": 2.5,
    "gpt-4o-mini": 0.075,
    "gpt-4o-mini-2024-07-18": 0.075,
    "gpt-4o-2024-08-06": 1.25,
    "gpt-4o-2024-11-20": 1.25,

    "o1-mini": 1.5,
    "o1-preview": 7.5,
    "o1-mini-2024-09-12": 1.5,
    "o1-preview-2024-09-12": 7.5,

    # 硅基
    "llama-3.1-8b-instruct": 0.01,
    "meta-llama/Meta-Llama-3.1-8B-Instruct": 0.01,
    "llama-3.1-70b-instruct": 2,
    "meta-llama/Meta-Llama-3.1-70B-Instruct": 2,
    "llama-3.1-405b-instruct": 5,
    "meta-llama/Meta-Llama-3.1-405B-Instruct": 5,
    "llama-3.1-nemotron-70b-instruct": 2,
    "nvidia/Llama-3.1-Nemotron-70B-Instruct": 2,

    "hunyuan-a52b-instruct": 2.5,  # 10.5

    # groq https://console.groq.com/docs/models
    "llama3-8b-8192": 0.01,
    "llama3-70b-8192": 0.01,
    "mixtral-8x7b-32768": 0.01,
    "gemma-7b-it": 0.01,
    "llama-3.1-8b-instant": 0.01,
    "llama-3.1-70b-versatile": 3,

    # sili
    "gemma2-9b-it": 0.01,
    "gemma2-27b-it": 0.63,
    "google/gemma-2-27b-it": 0.09,

    "internlm2_5-7b-chat": 0.01,
    'internlm2_5-20b-chat': 0.5,

    "acge_text_embedding": 1,
    "dmeta-embedding-zh-q4": 1,

    # vision 视觉
    "minicpm-v": 0.35 / 2,
    "minicpm-v2.6": 0.35 / 2,
    "llama-3.2-11b-vision": 0.1,

    "internvl2-8b": 0.35 / 2,
    "internvl2-26b": 1 / 2,
    "internvl2-llama3-76b": 4.13 / 2,

    "qwen2-vl-7b-instruct": 0.35 / 2,
    "qwen2-vl-72b-instruct": 4.13 / 2,
    "Qwen/Qwen2-VL-72B-Instruct": 4.13 / 2,

    # 临时
    "ep-20240515073409-dlpqp": 5

}

COMPLETION_RATIO = {
    # 智能体
    "gpt-4-plus": 5,
    "gpt-4o-plus": 5,

    "grok": 3,
    "grok-beta": 3,
    "x-ai/grok-beta": 3,
    "grok-vision-beta": 3,

    "claude-3-5-haiku-20241022": 5,
    "anthropic/claude-3-5-haiku-20241022:beta": 5,

    "gpt-4-all": 4,
    "gpt-4-gizmo-*": 4,
    "gpt-4o-all": 4,
    "o1-mini": 4,
    "o1-preview": 4,
    "o1-mini-2024-09-12": 4,
    "o1-preview-2024-09-12": 4,
    "gpt-4o-realtime-preview": 4,
    "gpt-4o-realtime-preview-2024-10-01": 4,
    "gpt-4o-2024-11-20": 4,

    # claude
    "claude-3-opus-20240229": 5,
    "anthropic/claude-3-opus:beta": 5,  # openrouter

    "anthropic/claude-3.5-sonnet": 5,
    "anthropic/claude-3.5-sonnet:beta": 5,

    "llama-3.1-70b-instruct": 2,
    "meta-llama/Meta-Llama-3.1-70B-Instruct": 2,

    "llama-3.1-405b-instruct": 6,
    "meta-llama/Meta-Llama-3.1-405B-Instruct": 6,

    "command": 4,
    "command-light": 4,
    "command-light-nightly": 4,
    "command-nightly": 4,
    "command-r": 4,
    "command-r-plus": 4,

    "command-r-08-2024": 4,
    "command-r-plus-08-2024": 4,

    "ERNIE-Speed-8K": 3,
    "ERNIE-Speed-128K": 3,

    "ERNIE-3.5-8K": 3,
    "ERNIE-3.5-128K": 3,

    "ERNIE-4.0-Turbo-8K": 3,
    "ERNIE-4.0-8K": 3,

    "gemini-1.5-pro-001": 4,
    "gemini-1.5-pro-002": 4,
    "gemini-1.5-flash-002": 4,

    "hunyuan-a52b-instruct": 5,
    "qwen2.5-coder-32b-instruct": 2,

    "qwen-turbo-2024-11-01": 3,
    "qwen/qwq-32b-preview": 2,
    "Qwen/QwQ-32B-Preview": 2,

}

REDIRECT_MODEL = {
    # https://docs.siliconflow.cn/docs/4-api%E8%B0%83%E7%94%A8
    "gpt-3.5-turbo": "THUDM/glm-4-9b-chat",  # 永久免费
    # "gpt-4o-mini": "THUDM/glm-4-9b-chat",  # 永久免费

    "chatfire-translator": "Qwen/Qwen2.5-7B-Instruct",  # 永久免费
    "internlm2_5-7b-chat": "internlm/internlm2_5-7b-chat",  # 永久免费

    "glm-3-turbo": "THUDM/glm-4-9b-chat",  # 永久免费
    "glm-4-air": "THUDM/glm-4-9b-chat",  # 永久免费
    "glm-4-flash": "THUDM/glm-4-9b-chat",  # 永久免费
    'glm-4-9b-chat': 'THUDM/glm-4-9b-chat',  # 永久免费
    'chatglm3-6b': 'THUDM/chatglm3-6b',  # 永久免费

    "doubao-pro-128k": "deepseek-ai/DeepSeek-V2-Chat",
    # "deepseek-chat": "deepseek-ai/DeepSeek-V2-Chat",
    "deepseek-chat": "deepseek-ai/DeepSeek-V2.5",

    "deepseek-coder": "deepseek-ai/DeepSeek-Coder-V2-Instruct",
    'deepseek-coder-v2-instruct': 'deepseek-ai/DeepSeek-Coder-V2-Instruct',
    'deepseek-v2-chat': 'deepseek-ai/DeepSeek-V2-Chat',
    "deepseek-v2.5-chat": "deepseek-ai/DeepSeek-V2.5",
    'deepseek-llm-67b-chat': 'deepseek-ai/deepseek-llm-67b-chat',

    "yi-spark": "01-ai/Yi-1.5-9B-Chat-16K",  # 永久免费
    "yi-medium": "01-ai/Yi-1.5-9B-Chat-16K",  # 永久免费
    "yi-large-turbo": "01-ai/Yi-1.5-9B-Chat-16K",  # 永久免费

    'yi-1.5-6b-chat': '01-ai/Yi-1.5-6B-Chat',  # 永久免费
    'yi-1.5-9b-chat-16k': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    'yi-34b-chat': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    'yi-34b-chat-0205': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    'yi-1.5-34b-chat-16k': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    # 'yi-1.5-34b-chat-16k': '01-ai/Yi-1.5-34B-Chat-16K',

    "yi-lightning": "yi-lightning",
    "yi-large": "yi-lightning",
    "yi-large-rag": "yi-lightning",
    "yi-large-fc": "yi-lightning",
    "yi-medium-200k": "yi-lightning",

    # Vision
    "llama-3.2-11b-vision": "meta-llama/Llama-Vision-Free",

    # InternVL2
    "internvl2-8b": "Pro/OpenGVLab/InternVL2-8B",
    "internvl2-26b": "OpenGVLab/InternVL2-26B",
    "internvl2-llama3-76b": "OpenGVLab/InternVL2-Llama3-76B",

    # 千问
    "minicpm-v": "Pro/Qwen/Qwen2-VL-7B-Instruct",
    "minicpm-v2.6": "Pro/Qwen/Qwen2-VL-7B-Instruct",
    "qwen2-vl-7b-instruct": "Pro/Qwen/Qwen2-VL-7B-Instruct",
    "qwen2-vl-72b-instruct": "Qwen/Qwen2-VL-72B-Instruct",

    "qwen2.5-7b-instruct": "Qwen/Qwen2.5-7B-Instruct",
    "qwen2.5-14b-instruct": "Qwen/Qwen2.5-14B-Instruct",
    "qwen2.5-32b-instruct": "Qwen/Qwen2.5-32B-Instruct",
    "qwen2.5-72b-instruct": "Qwen/Qwen2.5-72B-Instruct",
    "qwen2.5-math-72b-instruct": "Qwen/Qwen2.5-Math-72B-Instruct",
    "qwen2.5-coder-7b-instruct": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "qwen2.5-coder-32b-instruct": "Qwen/Qwen2.5-Coder-32B-Instruct",

    "qwen-turbo": "Qwen/Qwen2-7B-Instruct",
    'qwen2-1.5b-instruct': 'Qwen/Qwen2-1.5B-Instruct',
    'qwen2-7b-instruct': 'Qwen/Qwen2-7B-Instruct',
    'qwen2-72b-instruct': 'Qwen/Qwen2-72B-Instruct',
    'qwen2-math-72b-instruct': 'Qwen/Qwen2-Math-72B-Instruct',

    'qwen2-57b-a14b-instruct': 'Qwen/Qwen2-57B-A14B-Instruct',
    'qwen1.5-7b-chat': 'Qwen/Qwen1.5-7B-Chat',
    'qwen1.5-14b-chat': 'Qwen/Qwen1.5-14B-Chat',
    'qwen1.5-32b-chat': 'Qwen/Qwen1.5-32B-Chat',
    'qwen1.5-110b-chat': 'Qwen/Qwen1.5-110B-Chat',

    'internlm2_5-20b-chat': 'internlm/internlm2_5-20b-chat',

    # 千问兜底
    "qwen-max": 'Qwen/Qwen2.5-72B-Instruct',
    "qwen-plus": 'Qwen/Qwen2.5-72B-Instruct',

    # 国外开源
    "gemma2-9b-it": "google/gemma-2-9b-it",  # 永久免费
    "gemma2-27b-it": "google/gemma-2-27b-it",
    "gemini": "google/gemma-2-9b-it",  # todo
    "gemini-1.5": "google/gemma-2-27b-it",

    "meta-llama-3-8b-instruct": "meta-llama/Meta-Llama-3-8B-Instruct",  # 永久免费
    "mistral-7b-instruct": "mistralai/Mistral-7B-Instruct-v0.2",  # 永久免费

    "mixtral-8x7b-instruct-v0.1": "mistralai/Mixtral-8x7B-Instruct-v0.1",

    "meta-llama-3-70b-instruct": "meta-llama/Meta-Llama-3-70B-Instruct",
    "llama-3-70b-instruct": "meta-llama/Meta-Llama-3-70B-Instruct",
    "llama-3.1-8b-instruct": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "llama-3.1-70b-instruct": "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "llama-3.1-405b-instruct": "meta-llama/Meta-Llama-3.1-405B-Instruct",

    "llama-3.1-nemotron-70b-instruct": "nvidia/Llama-3.1-Nemotron-70B-Instruct",

    # https://xinghuo.xfyun.cn/sparkapi
    # spark-lite,spark-pro,spark-max,spark-ultra
    # 'spark-lite': "general",  # 实名免费
    'spark-lite': "generalv3.5",  # 实名免费
    'spark-pro': "generalv3.5",
    'spark-pro-128k': "generalv3.5",
    'spark-max': "generalv3.5",
    'spark-ultra': "generalv3.5",

    # 硅基
    "hunyuan-a52b-instruct": "Tencent/Hunyuan-A52B-Instruct",

    "stable-diffusion": "stabilityai/stable-diffusion-3-medium",
    "stable-diffusion-3-medium": "stabilityai/stable-diffusion-3-medium",

    "stable-diffusion-turbo": "stabilityai/sd-turbo",
    "stable-diffusion-xl-turbo": "stabilityai/sdxl-turbo",
    "dreamshaper-8-lcm": "ByteDance/SDXL-Lightning",

    "stable-diffusion-v1-5-img2img": "ByteDance/SDXL-Lightning",
    "stable-diffusion-2-1": "stabilityai/stable-diffusion-2-1",
    "stable-diffusion-xl-base-1.0": "stabilityai/stable-diffusion-xl-base-1.0",
    "stable-diffusion-xl-lightning": "ByteDance/SDXL-Lightning",
    "stable-diffusion-3": "stabilityai/stable-diffusion-3-medium",

    "photomaker": "TencentARC/PhotoMaker",

    "flux.1-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux.1-dev": "black-forest-labs/FLUX.1-dev",

    # groq
    # "llama3-8b": "llama3-8b-8192",
    # "mixtral-8x7b": "mixtral-8x7b-32768",
    # "gemma-7b": "gemma-7b-it",
    # "gemma2-9b": "gemma2-9b-it"

    "todo": "gpt-4-vision-preview",

    # https://chat.tune.app/api/models
    "claude-3-haiku-20240307": "anthropic/claude-3-haiku",
    "claude-3-5-sonnet-20240620": "anthropic/claude-3.5-sonnet",
    "gpt-4o": "openai/gpt-4o",
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "mistral-large": "mistral/mistral-large",
    "o1-mini": "openai/o1-mini",

    "o1-preview": "openai/o1-preview",
    # "qwen-2-vl-72b": "qwen/qwen-2-vl-72b",
    # "qwen-2.5-72b": "qwen/qwen-2.5-72b",
    "tune-blob": "kaushikaakash04/tune-blob",
    "tune-mythomax-l2-13b": "rohan/tune-mythomax-l2-13b",
    "tune-wizardlm-2-8x22b": "rohan/tune-wizardlm-2-8x22b"

}

GROUP_RATIO = {
    "chatfire": 1,

    "default": 1,

    "特价": 0.5,  # 包含逆向等模型

    "vip3": 3,
    "vip8": 8,

    "国产": 0.5,

    "2B": 4,

    # 定制分组：不公开
    "35": 1,

    "agent": 2

}
USER_USABLE_GROUPS = {
    "default": "1.0￥=1$默认分组-全模型",

    "vip3": "3.0￥=1$直连",
    "vip8": "8.0￥=1$直连❤️不计成本保证稳定性",
    "国产": "0.5￥=1$直连🔥国产大模型api，可申请商用独立分组",

    "特价": "0.5￥=1$主打性价比🔥claude系列&gpt/o1系列&国产热门大模型",

    "agent": "2.0￥=1$智能体：联网&文件问答",

}

if _ := {k: f"888￥=1$🈲🈲🈲误用不退" for k, v in GROUP_RATIO.items() if k.endswith(("代理",))}:
    USER_USABLE_GROUPS = {**USER_USABLE_GROUPS, **_}

# https://oss.ffire.cc/images/qw.jpeg?x-oss-process=image/format,jpg/resize,w_512
if __name__ == '__main__':
    # print(','.join(REDIRECT_MODEL.keys()))

    from meutils.apis.oneapi import option, channel

    option()
    #
    arun(channel.edit_channel(MODEL_PRICE))
