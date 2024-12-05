# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import abc
import os
import sys

from django.core.exceptions import ValidationError


class BaseValidator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def validate(self, *args, **kwargs):
        """
        对应的校验逻辑
        """


class EnvValidator(BaseValidator):
    ENV_SETTINGS = {
        "open_v2": ("BK_PAAS_HOST", "APP_ID", "APP_TOKEN"),
        "open_v3": (
            "BK_PAAS2_URL",
            "BKPAAS_MAJOR_VERSION",
            "BKPAAS_APP_ID",
            "BKPAAS_APP_SECRET",
            "BK_COMPONENT_API_URL",
        ),
        "ieod": (
            "BKPAAS_APP_ID",
            "BKPAAS_APP_SECRET",
            "BKPAAS_LOGIN_URL",
            "BKPAAS_REMOTE_STATIC_URL",
            "BKPAAS_APIGW_OAUTH_API_URL",
        ),
        "tencent": (
            "BKPAAS_APP_ID",
            "BKPAAS_APP_SECRET",
            "BKPAAS_LOGIN_URL",
            "BKPAAS_REMOTE_STATIC_URL",
            "BKPAAS_APIGW_OAUTH_API_URL",
        ),
    }
    VALID_RUN_VER = ("ieod", "open", "tencent")

    def __init__(self, run_ver):
        if run_ver not in self.VALID_RUN_VER:
            raise ValidationError(f'run_ver值不合法，合法的值有：{",".join(self.VALID_RUN_VER)}')

        self.run_ver = run_ver

    def _check_env(self, env_settings_key):
        return [
            env for env in self.ENV_SETTINGS[env_settings_key] if os.getenv(env) is None
        ]

    def validate(self, *args, **kwargs):
        needed_envs = []

        if self.run_ver in self.ENV_SETTINGS:
            needed_envs = self._check_env(self.run_ver)
        elif self.run_ver == "open":
            env_settings_key = (
                "open_v3"
                if int(os.getenv("BKPAAS_MAJOR_VERSION", 2)) == 3
                else "open_v2"
            )
            needed_envs = self._check_env(env_settings_key)

        if needed_envs:
            sys.stderr.write(
                f"当前运行环境缺少部分需要的环境变量，可能导致项目运行报错，"
                f'请确认以下环境变量已经配置并赋值: {",".join(needed_envs)}\n'
            )
            if self.run_ver == "open":
                sys.stderr.write("注意，当前版本为社区版环境，请确认 BKPAAS_MAJOR_VERSION 已经配置并正确赋值\n")
