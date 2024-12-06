#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : nacos
# @Time         : 2024/4/17 17:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/nacos-group/nacos-sdk-python
# https://baijiahao.baidu.com/s?id=1774464887530962175&wfr=spider&for=pc

from meutils.pipe import *
import nacos  # nacos-sdk-python

# Both HTTP/HTTPS protocols are supported, if not set protocol prefix default is HTTP, and HTTPS with no ssl check(verify=False)
# "192.168.3.4:8848" or "https://192.168.3.4:443" or "http://192.168.3.4:8848,192.168.3.5:8848" or "https://192.168.3.4:443,https://192.168.3.5:443"
server_addresses = "nacos.chatfire.cc"
NAMESPACE = "test"

# no auth mode
client = nacos.NacosClient(server_addresses=server_addresses, namespace=NAMESPACE, username='chatfire', password='chatfirechatfire')
# auth mode
# client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, ak="{ak}", sk="{sk}")

# get config
data_id = "testdata"
group = "DEFAULT_GROUP"
print(client.get_config(data_id, group))


