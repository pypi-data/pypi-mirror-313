#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : config_manager
# @Time         : 2024/12/4 12:07
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import nacos
import yaml

from meutils.pipe import *

class ConfigManager:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Nacos客户端配置
        self.client = nacos.NacosClient(
            server_addresses="nacos.chatfire.cc",  # Nacos服务器地址
            namespace="test",  # 命名空间
            username="chatfire",  # 用户名
            password="chatfirechatfire"  # 密码
        )

    def init_config(self, data_id: str, group: str = "DEFAULT_GROUP"):
        """初始化配置并添加监听器"""
        # 获取初始配置
        config = self.client.get_config(data_id, group)
        logger.debug(config)

        if config:
            self._config = yaml.safe_load(config)

        # 添加配置变更监听器
        self.client.add_config_watcher(
            data_id,
            group,
            self._config_changed_callback
        )

    def _config_changed_callback(self, args):
        """配置变更回调函数"""
        print(f"配置发生变更: {args}")
        try:
            self._config = yaml.safe_load(args['content'])
            print(f"最新配置: {self._config}")
        except Exception as e:
            print(f"配置更新失败: {e}")

    @property
    def config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return self._config


if __name__ == '__main__':
    # 初始化配置管理器

    data_id = "testdata"
    group = "DEFAULT_GROUP"

    config_manager = ConfigManager()
    config_manager.init_config(
        data_id=data_id,  # 配置ID
    )

    # yaml.safe_load("- 1")
