#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : check_utils
# @Time         : 2024/9/30 13:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators.retry import retrying

from openai import OpenAI, AsyncOpenAI


async def check_tokens(tokens, check_token: Callable):
    r = []
    for batch in tqdm(list(tokens) | xgroup(32)):
        bools = await asyncio.gather(*map(check_token, batch))
        r += list(itertools.compress(batch, bools))
    return r


@retrying()
@alru_cache(ttl=60)
async def check_token_for_siliconflow(api_key, threshold: float = 0):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_siliconflow)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    try:
        async with httpx.AsyncClient(headers=headers, timeout=60) as client:
            response: httpx.Response = await client.get("https://api.siliconflow.cn/v1/user/info")
            response.raise_for_status()

            logger.debug(response.text)
            logger.debug(response.status_code)

            if response.is_success:
                total_balance = response.json()['data']['totalBalance']
                return float(total_balance) >= threshold

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
async def check_token_for_openai(api_key, base_url="https://api.stepfun.com/v1"):
    try:
        client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        models = await client.models.list()
        logger.debug(models)
        return True

    except Exception as e:
        logger.error(e)
        return False


@retrying()
async def check_token_for_jina(api_key, threshold=1000):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_jina)

    params = {
        "api_key": api_key,  # "jina_c8da77fed9704d558c8def39837960edplTLkNYrsPTJHBF1HcYg_RkRVh0X"
    }

    try:
        async with httpx.AsyncClient(base_url="https://embeddings-dashboard-api.jina.ai/api/v1", timeout=60) as client:
            response: httpx.Response = await client.get("/api_key/user", params=params)
            response.raise_for_status()

            logger.debug(response.text)
            logger.debug(response.status_code)

            if response.is_success:
                data = response.json()
                total_balance = data['wallet']['total_balance']
                return float(total_balance) >= threshold

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


if __name__ == '__main__':
    from meutils.config_utils.lark_utils import get_next_token_for_polling

    pass
    arun(check_token_for_siliconflow("sk-xcdcquzwbsycxgadtwijeetzukhroyeorzqqzfvrtwrlmqrs"))

    FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=KVClcs"

    # b = arun(check_token_for_openai(os.getenv("STEP_API_KEY")))

    # arun(get_next_token_for_polling(check_token=check_token_for_openai, feishu_url=FEISHU_URL))

    arun(check_token_for_jina(["jina_c8da77fed9704d558c8def39837960edplTLkNYrsPTJHBF1HcYg_RkRVh0X"]*10))
