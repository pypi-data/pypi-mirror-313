#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2024/10/28 20:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import jwt
import time
import datetime

# Header and payload
header = {
    "alg": "HS256",
    "typ": "JWT"
}

payload = {
    "exp": int(time.time()) + 3600,  # 1 hour from now
    "user": {
        "id": "302833867771949058",
        "name": "me better",
        "avatar": "https://lh3.googleusercontent.com/a/ACg8ocIgSSChs1D4sTj1STk7PsTm7y53JDX99o8BxpZcV6560AJbRg=s96-c",
        "deviceID": ""
    }
}

# Your secret key
secret = ""

# Create the JWT
token = jwt.encode(payload, secret, algorithm="HS256", headers=header)

print(token)

jwt.decode(token, secret, algorithms=["HS256"])
