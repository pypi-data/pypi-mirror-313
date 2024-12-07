#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : vidu_video
# @Time         : 2024/7/31 08:59
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo 测试 https://oss-shanghai.sanwubeixin.cn/ios/110580373/20241126133701.png
import asyncio

from meutils.pipe import *
from meutils.decorators.retry import retrying

from meutils.schemas.vidu_types import BASE_URL, UPLOAD_BASE_URL, ViduRequest, ViduUpscaleRequest
from meutils.schemas.task_types import TaskType, Task, FileTask

from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling, get_spreadsheet_values

# FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=l3VpZf"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=V84y6z"
FEISHU_URL_VIP = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=EYgZ8c"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


async def upload(file, token: Optional[str] = None, vip: bool = False):  # todo: 统一到 file object
    token = token or await get_next_token_for_polling(
        FEISHU_URL_VIP if vip else FEISHU_URL,
        check_token=check_token,
        from_redis=True,
        min_points=4  # 最小消耗
    )

    token = token.strip(";Shunt=").strip("; Shunt=")
    logger.debug(token)

    payload = {"scene": "vidu"}
    headers = {
        "Cookie": token  # ;Shunt= 居然失效
    }
    async with httpx.AsyncClient(base_url=UPLOAD_BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/files/uploads", json=payload)
        if response.is_success:
            logger.debug(response.json())
            file_id = response.json()['id']
            put_url = response.json()['put_url']  # 图片url

            response = await client.put(put_url, content=file, headers=headers)
            etag = response.headers.get('Etag')

            payload = {"id": file_id, "etag": etag}
            response = await client.put(f"/files/uploads/{file_id}/finish", json=payload)
            logger.debug(response.text)
            logger.debug(response.status_code)
            logger.debug(put_url.split('?')[0])
            if response.is_success:
                uri = response.json()['uri']
                return FileTask(id=file_id, url=put_url, system_fingerprint=token)

            response.raise_for_status()


@retrying(max_retries=8, max=8, predicate=lambda r: r is True, title=__name__)  # 触发重试
async def create_task(request: ViduRequest, token: Optional[str] = None, vip: bool = False):
    token = token or await get_next_token_for_polling(
        FEISHU_URL_VIP if vip else FEISHU_URL,
        check_token=check_token,
        from_redis=True,
        min_points=4  # 最小消耗
    )

    token = token.strip(";Shunt=").strip("; Shunt=")

    task_type = TaskType.vidu_vip if vip else TaskType.vidu

    headers = {
        "Cookie": token
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/tasks", json=request.payload)

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.status_code in {429, 403} or "insufficient" in response.text:  # 触发重试
            return True

        if response.is_success:
            data = response.json()
            task_id = f"{task_type}-{data['id']}"
            return Task(id=task_id, data=data, system_fingerprint=token)
        else:
            logger.debug(token)
            return Task(data=response.text, status=0, status_code=response.status_code)


@retrying(max_retries=8, max=8, predicate=lambda r: r is True, title=__name__)  # 触发重试
async def create_task_upscale(request: ViduUpscaleRequest, token: str):
    payload = {
        "input": {
            "creation_id": str(request.creation_id)
        },
        "type": "upscale",
        "settings": {"model": "stable", "duration": 4}  #######
    }
    headers = {
        "Cookie": token
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/tasks", json=payload)

        if response.status_code in {429} and "insufficient" in response.text:  # 触发重试
            return True

        if response.is_success:
            data = response.json()
            task_id = f"vidu-{data['id']}"
            return Task(id=task_id, data=data, system_fingerprint=token)
        else:
            return Task(data=response.text, status=0, status_code=response.status_code)


@retrying(max_retries=3, title=__name__)
async def get_task(task_id: str, token: str):  # https://api.vidu.studio/vidu/v1/tasks/state?id=2375528561004183
    task_id = task_id.split("-", 1)[-1]

    token = token.strip(";Shunt=").strip("; Shunt=")

    headers = {
        "Cookie": token
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.get(f"/tasks/{task_id}")

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()
            return data
        response.raise_for_status()


@retrying(title=__name__)
@alru_cache(ttl=10)
async def get_credits(token: str):
    headers = {
        "Cookie": token.rstrip(";Shunt=").strip("; Shunt="),
    }

    async with httpx.AsyncClient(headers=headers, timeout=60) as client:
        response = await client.get("https://api.vidu.studio/credit/v1/credits/me")
        logger.debug(response.status_code)
        logger.debug(response.text)

        if response.is_success:
            data = response.json()
            # {
            #     "credits": 1952,
            #     "credits_expire_today": 0,
            #     "credits_expire_monthly": 1936,
            #     "credits_permanent": 16
            # }
            return data
        response.raise_for_status()


async def check_token(token, threshold: float = 0):
    try:
        data = await get_credits(token)
        logger.debug(data['credits'])
        return data['credits'] > threshold  # 视频
    except Exception as e:
        logger.error(e)
        logger.debug(token)
        return False


if __name__ == '__main__':
    token = "sajssdk_2015_cross_new_user=1; _ga=GA1.1.338141957.1727086892; Shunt=; JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjgzODMxMDYsImlhdCI6MTcyNzA4NzEwNiwiaXNzIjoiaWFtIiwic3ViIjoiMjQxNjY4MjA0OTYxNDUwNCJ9.Av3Uz9wG0L9ENvClhC9repoRthUm8wgspT5pWcmqaqs; _ga_ZJBV7VYP55=GS1.1.1727086892.1.1.1727087109.0.0.0; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22sSEnntsASGnESHAS%22%2C%22gae28_aV%22%3A%22EGsErnnGsGuGiH-AtVyGiIuniVIEg-snAAEEHE-EIsREAS-EGsErnnGsGyuyy%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlcwZKsQqlcpZ3HPFK8wXzlPhkzws3sPZNhwZP8wqPMwX1JQF18wFwcQh1MQvAJpF3JWFPspF3HPsxqPc323a7OW9dbV9kArdG2usVOukGOWv3n3q3AwFPspX3MQXlswFNEwXNagN%3D%3D%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%24aVr68a8c_kmfa6_aV%22%2C%22Cikbr%22%3A%22sSEnntsASGnESHAS%22%7D%7D"
    # FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=Hcr2i8"
    # arun(get_next_token_for_polling(FEISHU_URL, check_token=check_token))
    # arun(get_next_token_for_polling(FEISHU_URL_VIP, check_token=check_token, max_size=10000))

    # token = "_GRECAPTCHA=09AEXsBHm3ZGyFm6bsaF_HVQw8tBthjXeptYzdw7mGCczOlla0LlYHSb_HESN_xn3uXXR55VaHqXzc8EN2-0eCjQs; io=cmL_418SiY874dz6Ac4C; HMACCOUNT_BFESS=3B0B5E02E41153CB; Hm_lvt_a3c8711bce1795293b1793d35916c067=1725242991; Hm_lpvt_a3c8711bce1795293b1793d35916c067=1725242991; HMACCOUNT=3B0B5E02E41153CB; _ga=GA1.1.793646133.1725242994; sajssdk_2015_cross_new_user=1; JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjY1MzkwMDAsImlhdCI6MTcyNTI0MzAwMCwiaXNzIjoiaWFtIiwic3ViIjoiMjQxNTEwMzE4NzgwNTkzMSJ9.AW77pOYME2EePiEV4TmtViBWPvPw_2tiY73R5s2APe8; Shunt=; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22sSEHEAIEtRtAHGIE%22%2C%22gae28_aV%22%3A%22EGEuARrrVIArig-AgnEgGiVVIyAyit-EuHsHnIR-GsEnAA-EGEuARrrVIEERSE%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlJPq0IWZdlwhLkPZP8w9PswZPHPZ7lwswMPs1SBFTaQF3EQqwIBFlcwFPMwvAJpFTawXVkWZNhwF1IQX1aBv3liZ7ku67OV5kgu9G6iZHgiZNapa3cQX1EwF0hwFfIpX0EpFwJ36A%3D%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%24aVr68a8c_kmfa6_aV%22%2C%22Cikbr%22%3A%22sSEHEAIEtRtAHGIE%22%7D%7D; SERVERCORSID=75eeb9319017a9014e79152a283d6cbe|1725243001|1725242994; _ga_ZJBV7VYP55=GS1.1.1725242993.1.1.1725243001.0.0.0"
    #
    # token = '_GRECAPTCHA=09AA5Y-DKEaPCPtfl_s0o9z-HKEP5Tkfrn7CsmZfUj5MUYAFZiW7ELincbr2c2baFkM5Vu_KDPJ11l_N_DJhHTx_A; HMACCOUNT_BFESS=4189E6AE98589913; Hm_lvt_a3c8711bce1795293b1793d35916c067=1722407159; Hm_lpvt_a3c8711bce1795293b1793d35916c067=1722407159; HMACCOUNT=4189E6AE98589913; io=FKh7a-dvlK-UnBmOAB7M; JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjM3MDMxNjgsImlhdCI6MTcyMjQwNzE2OCwiaXNzIjoiaWFtIiwic3ViIjoiMjM2ODY0MDkxNDEwMTMxOCJ9.mbNkzI6piihIVDsGSshSCiLlakAAG_Hxh0xAnPkx_vs; Shunt=; Hm_lvt_a3c8711bce1795293b1793d35916c067=1753943158594|1722407159; shortid=parsvjrji; debug=undefined; _grecaptcha=09AA5Y-DJauC2Mo_KPc5_R5OUPR__wsqLYpOjUViIajU8hpDPOpg6LcH1xECbelcZwXl_BSHnZlCWRGxGWvRvMyQr7QGnCCJam75DKvw; VIDU_SELECTED_LOCALE=zh; VIDU_TOUR="v1"'
    # token = "JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjM3MDIyNjAsImlhdCI6MTcyMjQwNjI2MCwiaXNzIjoiaWFtIiwic3ViIjoiMjM2ODYyNjA0MzE4MTg1NCJ9.8P8WuktyjFM0utFbGcxLQptzfv43ugmMcE31RXR9JJQ"
    file = Path('/Users/betterme/PycharmProjects/AI/cover.jpeg').read_bytes()
    # url = arun(upload(file, vip=True)).url

    # print(arun(get_next_token_for_polling(FEISHU_URL)) == token)

    # arun(get_task("vidu-2368380300283813", token=token))
    # arun(get_task('vidu-2389570992698888', token=token))

    # arun(create_task_upscale())

    # token="_ga=GA1.1.2058758439.1724312077; Shunt=; JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjk5MTIxNDcsImlhdCI6MTcyODYxNjE0NywiaXNzIjoiaWFtIiwic3ViIjoiMjQyNzk2NjczODQwNjY3OSJ9.VFLEBmnL8_Biy_46X19Fr5PkbwxdLXx3Xq2GagsW2Fw; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22sSsRGnnRItSAnnRG%22%2C%22gae28_aV%22%3A%22EGEuAnststSEirt-ARSAigSVHIiHVs-EtHsHnIR-sARInAA-EGEuAnststHsIti%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24ki8r28_ergreere%22%3A%22z88O2%3A%2F%2Fiyymb682.fmmfkr.ymo%2F%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlJPq0swqfcpXNJPZKSBF0IQXLzWq7lQFQzQZNcBF1SQF3EQqwIBF3MQhwswX08wFlJPq0swqfcpXKcwhzz3aMax9klWZHAiD7HDsJCWskbDskl3qmawqNcQhlsQqyhpXNMQqPIp4xG%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%24aVr68a8c_kmfa6_aV%22%2C%22Cikbr%22%3A%22sSsRGnnRItSAnnRG%22%7D%7D; _ga_ZJBV7VYP55=GS1.1.1728614362.54.1.1728616189.0.0.0"
    # arun(get_credits(token))
    #
    d = {
        "prompt": "一条可爱的狗跑过来",
        # "url": url  # failed to save uploads
    }
    token = None
    # print(bjson(ViduRequest(**d).payload))
    # arun(create_task(ViduRequest(**d)))
    # arun(create_task(ViduRequest(**d), vip=False))
    # # pass
    # token = "sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22sSsAAnHAInAGEtIG%22%2C%22gae28_aV%22%3A%22EGEuAnststSEirt-ARSAigSVHIiHVs-EtHsHnIR-sARInAA-EGEuAnststHsIti%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlJPq0swqfcpXNJPZKSBF0IQXLzWq7lQFQzQZNcBF1SQF3EQqwIBF3MQhwswX08wFlJPq0swqfcpXKcwhzz3aMax9klWZHAiD7HDsJCWskbDskl3qmawqNcwX0sQF0hQq0HwFfhp4xG%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%24aVr68a8c_kmfa6_aV%22%2C%22Cikbr%22%3A%22sSsAAnHAInAGEtIG%22%7D%7D;_ga=GA1.1.2058758439.1724312077;_ga_ZJBV7VYP55=GS1.1.1727080335.38.1.1727080510.0.0.0;JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjgzNTAzODAsImlhdCI6MTcyNzA1NDM4MCwiaXNzIjoiaWFtIiwic3ViIjoiMjQyMDA2NTAzNjA5MTgzOSJ9.PkjQqjYB56vYetYwmlagnWn_6bSCwoxCjI7BjfelBOU;Shunt="
    # # token = "_ga=GA1.1.2058758439.1724312077; JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjgzNTAzODAsImlhdCI6MTcyNzA1NDM4MCwiaXNzIjoiaWFtIiwic3ViIjoiMjQyMDA2NTAzNjA5MTgzOSJ9.PkjQqjYB56vYetYwmlagnWn_6bSCwoxCjI7BjfelBOU; Shunt=; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22sSsAAnHAInAGEtIG%22%2C%22gae28_aV%22%3A%22EGEuAnststSEirt-ARSAigSVHIiHVs-EtHsHnIR-sARInAA-EGEuAnststHsIti%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlJPq0swqfcpXNJPZKSBF0IQXLzWq7lQFQzQZNcBF1SQF3EQqwIBF3MQhwswX08wFlJPq0swqfcpXKcwhzz3aMax9klWZHAiD7HDsJCWskbDskl3qmawqNcwX0sQF0hQq0HwFfhp4xG%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%24aVr68a8c_kmfa6_aV%22%2C%22Cikbr%22%3A%22sSsAAnHAInAGEtIG%22%7D%7D; _ga_ZJBV7VYP55=GS1.1.1727080335.38.1.1727080510.0.0.0"
    # token = "JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjgzNDkyNzQsImlhdCI6MTcyNzA1MzI3NCwiaXNzIjoiaWFtIiwic3ViIjoiMjQyMDg5NjA4MTIwNTkwNyJ9.MRXmSr48PifQgRN1-yTTu8d7Sq1An4OS7G5WoYpJ_PU"

    token = "io=5x6Cq-35yXpNNaTnARm4; HMACCOUNT_BFESS=B48B1DDD7D11A6A2; Hm_lvt_a3c8711bce1795293b1793d35916c067=1732425804; Hm_lpvt_a3c8711bce1795293b1793d35916c067=1732425804; HMACCOUNT=B48B1DDD7D11A6A2; NEXT_LOCALE=zh; _ga=GA1.1.1058503703.1732425808; _ga_ZJBV7VYP55=GS1.1.1732425807.1.0.1732425807.0.0.0; sajssdk_2015_cross_new_user=1; aws-waf-token=1d7ade76-9c93-45d6-a3b3-ef1923dd3313:AAoAinMlYBIIAAAA:aFvWrQSuG72jHptL59eihBkkJmExBqqNxdmwnrFfMkZWiarHlmuulrC2okyx3jUF1c1ODfG+Gf+itl0la/LUcmEa6RdrCJp32Fgq+TdA/TYSCknbdOcOtXUxuvI1RXrJV6kIn9zKn+NBtsMoWW4OlJgvniXCNeZu9gO9ZLFjmH4KQYB37hIZnzvRSnpa5fCENwMTt0UU+Th3Mu0ZoJP5lT920UqSimOR8mAG+xZc7JgsyIh0oxrGO8eCZDzmYjXI/O6BDIbO; JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM3MjE4MjEsImlhdCI6MTczMjQyNTgyMSwiaXNzIjoiaWFtIiwic3ViIjoiMjUzMjc4NjUyMTEyNzg0MSJ9.mZt9S7BTWCB_85FcajQtX4OoTr6CMghELVHnl7gt3zM; Shunt=; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22sHIsRtnHsEEsRtSE%22%2C%22gae28_aV%22%3A%22EGIHyGggREiRVA-AEusHsRSsinuuyr-EuHsHnIR-GsEnAA-EGIHyGggREuEgGA%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlhQZwHWoPIwZ1IWX08wXTawqKcQhNcPFWaPoQkBFTaQF3EQqwIBFlcwFPMwvAJpFwEPhkoWqyJPqTopF0aBv3liZ7ku67OV5kgu9G6iZHgiZNapa3cQFwcQhfsQF3JwF3IpXNJ36A%3D%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%24aVr68a8c_kmfa6_aV%22%2C%22Cikbr%22%3A%22sHIsRtnHsEEsRtSE%22%7D%7D; SERVERCORSID=75eeb9319017a9014e79152a283d6cbe|1732425821|1732425808"
    arun(check_token(token))
    #
    # FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=rxldsA"
    # FEISHU_URL="https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=Hcr2i8"
    # api_keys = get_spreadsheet_values(feishu_url=FEISHU_URL, to_dataframe=True)[0]
    #
    #
    # for i in tqdm(api_keys):
    #     logger.debug(i)
    #     if i and arun(check_token(i)):
    #         j = i
    #     # for j in (i or '').split(';'):
    #     #     if j.startswith('JWT='):
    #         with open('xx.txt', 'a') as f:
    #             f.write(j + '\n')
    # #
    # FEISHU_URL_VIP
    # arun(get_next_token_for_polling(FEISHU_URL_VIP,
    #                                 check_token=check_token,
    #                                 from_redis=True))

    # arun(get_next_token_for_polling(FEISHU_URL,
    #                                 check_token=check_token,
    #                                 from_redis=True))

    # from meutils.db.redis_db import redis_aclient

    # arun(redis_aclient.delete(FEISHU_URL))

    # token = "_ga=GA1.1.633410699.1728736789; Shunt=; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22sSRAsSHEntRnsHns%22%2C%22gae28_aV%22%3A%22EGstAuVggRArIr-AtnSIGARtIVIrSt-EnHsHnIR-EEtRAHn-EGstAuVggRErEt%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlcpXLaW9WoQhLkwsK8wXfsQXwHwXySwsNhWFNSBF1sQF3EQqwIBF1JpXyMQFP8wFlcpXLaW9WoQhTkwFfaBv3liZ7ku67OV5kgu9G6iZHgiZNapa3cQXyMwqNEwFPSQhPcQFPc36A%3D%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%24aVr68a8c_kmfa6_aV%22%2C%22Cikbr%22%3A%22sSRAsSHEntRnsHns%22%7D%7D; JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzIwMDM4NzAsImlhdCI6MTczMDcwNzg3MCwiaXNzIjoiaWFtIiwic3ViIjoiMjQ3MDI0NTE2ODc2MjU2MiJ9.uK3-CHB_6th4hha_IMI56KT7OLfwq8m-rOJCjwo0sxM; _ga_ZJBV7VYP55=GS1.1.1730707682.2.1.1730707881.0.0.0"
    #
    # arun(check_token(token))