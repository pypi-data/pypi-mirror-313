#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : auth
# @Time         : 2023/12/19 17:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from typing import Optional, Union

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

http_bearer = HTTPBearer()


# get_bearer_token = http_bearer


# 定义获取token的函数
async def get_bearer_token(
        auth: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
) -> Optional[str]:
    """
    获取Bearer token
    :param auth: HTTP认证凭证
    :return: token字符串
    """
    if auth is None:
        return None

    return auth.credentials


if __name__ == '__main__':
    pass
