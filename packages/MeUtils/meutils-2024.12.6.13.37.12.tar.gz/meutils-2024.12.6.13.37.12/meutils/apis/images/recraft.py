#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ecraft
# @Time         : 2024/10/31 16:30
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.io.files_utils import to_url
from meutils.schemas.image_types import ImageRequest, ImagesResponse, RecraftImageRequest
from meutils.notice.feishu import IMAGES, send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling, aget_spreadsheet_values
from meutils.decorators.retry import retrying

BASE_URL = "https://api.recraft.ai"

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=Lrhtf2"

DEFAULT_MODEL = "recraftv3"
MODELS = {}

send_message = partial(
    _send_message,
    title=__name__,
    url=IMAGES
)


@alru_cache(ttl=10 * 60)
@retrying()
async def get_access_token(token: Optional[str] = None):
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL, check_token=check_token)
    headers = {"cookie": token}

    async with httpx.AsyncClient(base_url="https://www.recraft.ai", headers=headers, timeout=60) as client:
        response = await client.get("/api/auth/session")
        response.raise_for_status()
        logger.debug(response.json())
        return response.json()["accessToken"]


# @retrying()
async def generate(request: RecraftImageRequest, token: Optional[str] = None):
    token = await get_access_token(token)
    headers = {"Authorization": f"Bearer {token}"}
    # params = {"project_id": "26016b99-3ad0-413b-821b-5f884bd9454e"}  # project_id 是否是必要的
    params = {}  # project_id 是否是必要的
    # params = {"project_id": "47ba6825-0fde-4cea-a17e-ed7398c0a298"}
    payload = request.model_dump(exclude_none=True)
    logger.debug(payload)

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(f"/queue_recraft/prompt_to_image", params=params, json=payload)
        response.raise_for_status()
        params = {
            "operation_id": response.json()["operationId"]
        }
        logger.debug(params)

        response = await client.get("/poll_recraft", params=params)
        response.raise_for_status()
        metadata = response.json()
        logger.debug(metadata)

        # {'credits': 1,
        #  'height': 1024,
        #  'images': [{'image_id': 'f9d8e7dd-c31f-4208-abe4-f44cdff050c2',
        #              'image_invariants': {'preset': 'any'},
        #              'transparent': False,
        #              'vector_image': False}],
        #  'random_seed': 1423697946,
        #  'request_id': '77bd917d-0960-4921-916f-038c773a41fd',
        #  'transform_model': 'recraftv3',
        #  'width': 1024}

        params = {"raster_image_content_type": "image/webp"}  #####
        params = {"raster_image_content_type": "image/png"}

        images = []
        for image in response.json()["images"]:
            response = await client.get(f"""/image/{image["image_id"]}""", params=params)
            url = await to_url(response.content)
            images.append(url)

        return ImagesResponse(image=images, metadata=metadata)


async def check_token(token, threshold: float = 1):
    if not isinstance(token, str):
        tokens = token
        r = []
        for batch in tqdm(tokens | xgroup(32)):
            bools = await asyncio.gather(*map(check_token, batch))
            r += list(itertools.compress(batch, bools))
        return r
    try:
        access_token = await get_access_token(token)
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
            response = await client.get("/users/me")
            response.raise_for_status()
            data = response.json()
            logger.debug(data["credits"])
            return data["credits"] >= threshold
    except Exception as e:
        logger.error(e)
        logger.debug(token)
        return False


if __name__ == '__main__':
    token = None
    # arun(get_access_token())
    request = RecraftImageRequest(
        prompt='一条猫'
    )
    arun(generate(request, token=token))

    # tokens = list(arun(aget_spreadsheet_values(feishu_url=FEISHU_URL, to_dataframe=True))[0]) | xfilter_

    # tokens = "__Host-next-auth.csrf-token=78920fc4c6bf5aef5c2063e3a4397b1e41074713e35020cf7049156e02d53355%7C2c8e6897101210b68ba31cec5c6232d8ab76a3e070cda7b82ad051680ab93fe0; _gcl_au=1.1.906962865.1730362257; _ga=GA1.1.435165527.1730362257; _fbp=fb.1.1730362257600.714008794112161913; AMP_MKTG_7268c9db0f=JTdCJTdE; _tt_enable_cookie=1; _pin_unauth=dWlkPU0yWmxPR1JsWkRJdE5qZGlZeTAwTWpNeUxXRmpNVEV0TlRrd1l6RTNZelEwTldZMw; __zlcmid=1OVn8OoYVNvKEWM; __stripe_mid=d21b2291-edb8-4cb1-8fac-05c6a9493ca8d85a3c; _ga_ME15C3DGRL=deleted; _ttp=412qSInHGw3jjdyNR6K4tBIYmNZ.tt.1; x-recraft-referral-code=3h7wfOgFGn; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.recraft.ai%2Fprojects; _clck=uflztg%7C2%7Cfra%7C0%7C1765; __Secure-next-auth.session-token.0=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..OMh8sDyFkAVpghZU.iIKkMX3OhmwVyO8CjwCH-8YFQE-J8zE52SImLqu-imuV9q0jNKxBDr9Zo-n2I-TdREv4ffj0FFagny27pL7vjMyp04X2VD_Lh5rv9OMAObho9TsX8AzyLZOu_xbXR1ip98ZSv432BcDq5ppm5ava-ZVqm0Tp0hvJGSWD1yq4S7XjqiIAGeKZfR5Efm1k85fO6CHp-nNiIFVc6f2sw0Y_DcfdAzB4tMxKmJPoa4VHteErM2n41XUA9TvftKK5xVLHDWi0poRXkfB6Tol2xF83jUi2f2Il1BzQ-7q-MsRD-kkxJkEbv2Zcex_HFsaFWN9ohDB_wttuDxBZYCwdjflE-XyLwurtLO4XwbZTRKOR0Jgl6SdF-tBgsKSUrDUdmPGt9oiZv-MzMpTiOYRhTFjTap34rjUOpqlCoPXtiI-YExDCuKs2Dy57wRHF5GHldb3-vuaxKV5tVIq3Uj0Z2uq1SRn2hFhbvcuywlHcyF9HnGur9M6-JBxDaS0W3hrhtHgegIj_kbe6Zl1KBT5knx_IDcVu3KXhiZaLI4kfn_3EQI5zZN9Ay6412fqjP1atd0BpeS5joJl_7O0ni8-0k1I6bRxhnD3uHD5dlQxBJXXHjyisoXTckUXNUKnRbc0x3pL0ObMP7VJ4-mov1KCc_YB3Msh0yfcIa_CXRTJCWH5Q-jkO0pJCVtWjfRegN8G-UpT9k3IDfu6z59O5qFYHM0SjFeee4yJNdAHJRpbuxxNBSBS8aIOey-UN-I2UDme_iGoQnkF9nvOI1zrVHtIhhazxc5YLOyDnVuyhI9ghm2PfYYIxp8sM-Y9VNPjuAKJvg6_q1tSVyiej-qHjV3um1n44AaChgrJ0JXU0gxQV_--xL2n28Tm4sOWb5VUGYAmI32Mvo5bC-kBatusIlkFvnfiQkZT-9fNPAfDiarG-W6T9VsLKhWn2UVBqSJtJgj56uCaw1QilqaKUSYGyUkStWEn0YXsye9vxKSDjm4LJTJdGlkKW0v4qElfwzzV0d9ErjohWN915IzVY-hTRSo8tgt_QHafO3hsyiTpGqalDuT_-BMBShRLozMvGhlQ9jA0QsDueosaNt9OWyk7ZliVSuyt17lI4ApFnaTf3MBjcrnUmk7aejOAQzuy5atNo-HmxxclEYsMuMblcp9kkAsrtx87RHrPYe7DmOorGqJRiKk27S2Nog5ZlBc8RAkq4u4eub9ezwMhFUAYKsv5tnaS6NiggXVbhNiN33uwk2jI7R9ZmJtCnw-b0Nnk2ln4_9CCSa8Ds9VMkiyS6S0QLaPlkmaBzgCYPM7sxTzyuw9BryOlo3akvYJHWegVvxWfN3ap8DdqgXE87zFPE3K3PmJodcv2lVz9FfwUtI81bwRkVpt4VNY7yqGNu33637cufapQsmZJilp5GfHv1FY1lXfrm0LQ19SUjgBHobZ6SrQPUcauypDNFOOAAt9MeVVScsY_5xcyRlPglsA31piiYnDcsBFwOIf-h5GxxYtqf8pDmvUMmXf1zn-97DLpa0D83rKFFA6BralkFCMq0gbBzH4CIeYW35-q1P9Ghq4FIxVxgreueSa5KP96BtFuzIuGEccN478JnsO-DkJWRzTToYTiNUieDjjuhQXFdOFooAHvTrEyvt0HM-ZchJcto4F6xKM3tuJAk2Ng9HCYiIy7rlYzW-gL0v07gI_hwKQ-8dOungh3ggfjooGSayAbsnLeRpAm3P9sTgKrnPp3fyBzzLDkpPj4wBxADpg4sYDyJk3hTa0ec9Kg4ssReU5K77vKg4-YkDAvKvYeQbX69FjXcHf1_XtBQVh2T-teb9G-0kAy6kLVarSJLjp6Mw_Uj3eYV9gbgmNiyBrCcHmUATA6FJkuxVH5W6YVChgEZgIYS1K-PZj-3uchfa6VoSCab1VnreJ6f5aYeY-4ZI5-vDwGJDpd2XkVIrf8zWPFqUkZRpyJHYRwXAGf8MCBFTRXBqzNgPnVjkh_iP9tbmb4_pbgBaTz3Izubx9lWUmso-y0_SPAn1M6x4V2zNHZR6ZVJKAxuNCQrqfIk0Q6-zFHdAHJFPrJSVjKMIDadIpxqQ5zkMeR0O6T204oVwfrtsMnuiAo3dk4ve5qa-MlaFyc0SpfxQkhzCTA3YVXKWo9G5Jp8OYBRmZwDhg4MTvgBeri-hyMsiS025J9vreey3BSyJun7IQJhzDZ6-PVO35qpVB65CNfNSDCO8rI_kAD8xKf893nHBovBumEU_FGC4xz6Yen-7W5TX4yR_2U2CBYX5Iplw5UXHgjXymPbfHjETIh_dyKnuN9fonl8fgi2xk5DDc-oyDaE1qq4g3oBMmXeFA8XpRvcOyXeDyYs5j-KiH0yMlel0xbFluk_UsuiElluUKx5IhnAf04-TX5SCmwubvssyTjs4bWeTw3rjwpvDV9EpLDgPt_WJnHgbbT7e9zRLqQWYnCGro8tnBVsLej-j73L4KdWJQeM8b-Q95l5TfhPrkmbUI-6qyV5tRawBO3ie-c836Bz7YUY1CnopG4qzUfZasJZ8ltrAr7qtwI1c-IJ6CAwDhT_SjhQwyMVUQb7OhvCryf5trtl29kVwsRCeuw8K9uVWmrAKIk5nf3IczDeKNpR0EEnpPMfblkEAaeCSz1KX2fSiURQ2GDUUAOICnhXEhJ9-NcNTHj4ssjU_8RAltnHxTiecwhsLX1qmxi0mrjf-32el6TgQ95FsNDRITKaZ1807lFiQnj3Um9Bqb8ZPxzBBEqJh0WKoD4xT1dqLc1f4HdebodGJva35Nw1Qc9ssNihz2Tziq56J1Zx8vOtz8ibmSJ6Gm3gzWD09h2CQN9Vxwx8kxmF_LECGwgkUsI77029-bayN_t2Mv_s3jeEOAQl-BBNMGHbPPPkcZi5siduzjpphVOAX8wOiqau0MqECstDqh8nemuSvhlomElxmU9mHiRTnUqlAfbO_P1581AUfyOh_InN3ydLnkgrziI58OEWIbHKXXEhRAcCGQrX4nynwOTymiWuzIR0OqhIyi3cLfz3e51uEVmBVVSZfbZuDySiY4yOzA2cMExG1te_NjjhEsvBZ8m3Fjf-PEwBJhrXDQgXlXFp80ERZQ6xVNzt7dVd0GzsQT1-03JaLR6S9tJYXO4QOf9sgXp-R4nvP7mZDuhP-kXbI0rzAmnuPA-eR4joGugTgbH0RWHnZ6z2a8k2kBD_VdjYdbxSZ1vRXtSIpNohuaun4rzXNbRz9kwNNK_Fz-q84fAJ_J1Yb1XHBMrJYQxwVdhRqvSh_jW5zroDFjTFNKwFruMaGa4KESccnTKy8mUH7Cd6S2OCjzDrcl4mQcXBu90FKOH-pYhobFNefJq6LooejPhdN_XBdfm2kQrcTRBYbMk4vekzZxs-wPrlgZkQYSAxKj4i_XTiqztmroaNRYdfFoq4hoArBBsISxRagLukwyL2yvSKnHiqMo9T7whwYF_tXQFGk1T8dQ_9ospLy9EMBMP7tdqw7UX5S051rqADt9q2Rozx7hRuAMHWeAyfRCFgMx0lR3B2txRxxRVWrBNJAqulmG3hJk9px8LpWmlm9CorOkN7cZT6CJKIJdSClkj0VDFiDUjWsZWJLiN_DSRaqcCpgwdkXJKZ4zpUKjH6xQSKzhvbmom9ZkFkNPWO35Vf7e_rLKLCyltHmsTDlgRylqPMkigL6Rds9S07c7fCwcr4d5xWvlV78iKjmg_c4RdxrmGsqeQZl4EmbnmwZfQj3qllIEn7MJ7N5_jE_BO1huH522Ds6hTRFTn_RmA4FtIbqyuvbK1v5MlCoToKiYgBwPI79PzQSEjM4LMMbeUiJx0E5C2Wd3bpTnbc-mfY8uIpFfxnK2_0Mk7rSbm8rqtomgPyqcmAT2mwQS-; __Secure-next-auth.session-token.1=DfJBMjFpUwPYqCIaGMxrX_WtlNau_0B5y61DkoPxCwi6_MziMSz6KUgDB9o4d6xXg5mn-UBR0gXWjPFrIXzP0kdNvCSF9pSGCyiOLmdtKfi3BscGIK70dpfUfKwY972YF6TTb6tXOdLkf3JFyN0cjLd5pcBfSKFAKRt5shH4iNMu6ZwgwZd0guK8IcIddc9KTGxTZlHc6dJ1Rc-QHfBm_DPgYUvf9yKjGSguPuYFqnHwA2T91Ughu9VT2lAuCKjvEX13KOsHB-Vr1i7Ts3TrQtIoS9pMM_NnhdILOp3Od5NGfkJGqAbsfFLYU193V3cK4cib9QisQmKm4hxvlMflKA1IQNlz_isB1vi2JN04AQg.z8GHyaN7ezsgo22MdsiVvQ; _uetsid=84c52090adf211efb65c0dc3b78a1976; _uetvid=a8a766f0975f11ef9b7921e48a0cd258; _ga_ME15C3DGRL=GS1.1.1732844258.46.1.1732845589.0.0.0; _clsk=c52eh1%7C1732845591268%7C3%7C0%7Ce.clarity.ms%2Fcollect; AMP_7268c9db0f=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI2OTE1YzI1My1jMTJjLTQ5ODYtYjM3Ni0xMTI3Y2ZmMTFlMjglMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJjNDdkY2ZiYi0yOWE5LTQ1Y2EtYWRiZS1hM2ZhYWZiODhkNzQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMyODQ0MjU3NzEzJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMjg0NTY0OTcyNSUyQyUyMmxhc3RFdmVudElkJTIyJTNBOTA1JTJDJTIycGFnZUNvdW50ZXIlMjIlM0E0JTdE"
    #
    # arun(check_token(tokens))
