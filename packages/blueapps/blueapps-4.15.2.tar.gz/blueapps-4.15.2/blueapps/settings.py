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

from django.conf import settings
from django.utils.module_loading import import_string

# 变量默认配置
DEFAULT_SETTINGS = {
    # ACCOUNT 相关配置会根据有无配置进行值覆盖，默认不提供，默认值可参考account/sites/default.py
    "ENABLE": {
        "OTEL": {
            "TRACE": False,
            "METRICS": False,
        }
    },
    "BKAPP": {
        "OTEL": {
            "SERVICE_NAME": getattr(settings, "APP_CODE", "Blueapps"),
            "BK_DATA_ID": -1,
            "SAMPLER": "parentbased_always_off",
            "GRPC_HOST": None,
            "BK_DATA_TOKEN": "",
            "LOGGING_TRACE_FORMAT": None,
            "INSTRUMENT_DB_API": False,
            "ADDTIONAL_INSTRUMENTORS": [],
            "SPAN_PROCESSOR": "blueapps.opentelemetry.export.LazyBatchSpanProcessor",
            "SERVICE_NAME_HANDLER": "blueapps.opentelemetry.utils.BlueappsServiceNameHandler",
        },
    },
    "IS_AJAX_PLAIN_MODE": False,
    "SPECIFIC_REDIRECT_KEY": None,
    "AJAX_401_RESPONSE_FUNC": None,
    "PAGE_401_RESPONSE_FUNC": None,
    "PAGE_401_RESPONSE_PLATFORM_FUNC": None,
    "NON_REQUEST_USERNAME_PROVIDER": None,
}

# 提供路径需要import_string的变量
IMPORT_SETTINGS = [
    "AJAX_401_RESPONSE_FUNC",
    "PAGE_401_RESPONSE_FUNC",
    "PAGE_401_RESPONSE_PLATFORM_FUNC",
    "BKAPP_OTEL_SPAN_PROCESSOR",
    "BKAPP_OTEL_SERVICE_NAME_HANDLER",
    "NON_REQUEST_USERNAME_PROVIDER",
]

# 在django_settings和blueapps_settings中都支持的配置项
BLUEAPPS_SUPPORT_DJANGO_SETTINGS = [
    "IS_AJAX_PLAIN_MODE",
    "ENABLE_OTEL_TRACE",
    "ENABLE_OTEL_METRICS",
    "BKAPP_OTEL_SERVICE_NAME",
    "BKAPP_OTEL_BK_DATA_ID",
    "BKAPP_OTEL_SAMPLER",
    "BKAPP_OTEL_GRPC_HOST",
    "BKAPP_OTEL_BK_DATA_TOKEN",
    "BK_APP_OTEL_ADDTIONAL_INSTRUMENTORS",
    "BK_APP_OTEL_INSTRUMENT_DB_API",
    "OTEL_LOGGING_TRACE_FORMAT",
    "BKAPP_OTEL_SPAN_PROCESSOR",
    "BKAPP_OTEL_SERVICE_NAME_HANDLER",
]


class BlueappsSettings:
    SETTING_PREFIX = "BLUEAPPS"
    NESTING_SEPARATOR = "_"

    def __init__(self, default_settings=None, import_strings=None):
        self.project_settings = self.get_flatten_settings(getattr(settings, self.SETTING_PREFIX, {}))
        self.project_settings.update(self.get_django_blueapps_settings())
        self.default_settings = self.get_flatten_settings(default_settings or DEFAULT_SETTINGS)
        self.import_strings = import_strings or IMPORT_SETTINGS

    def __getattr__(self, key):
        if key not in self.project_settings and key not in self.default_settings:
            raise AttributeError

        try:
            value = self.project_settings[key]
        except KeyError:
            value = self.default_settings[key]

        if key in self.import_strings and isinstance(value, str):
            try:
                value = import_string(value)
            except ImportError as e:
                message = f"Can not import {value} for Blueapps settings: {e}"
                raise ImportError(message)

        if value is not None:
            setattr(self, key, value)
        return value

    def get_flatten_settings(self, inputted_settings: dict, cur_prefix: str = ""):
        """获取BLUEAPPS配置字典打平之后的配置字典"""

        def get_cur_key(cur_key):
            return f"{cur_prefix}{self.NESTING_SEPARATOR}{cur_key}" if cur_prefix else cur_key

        flatten_settings = {}
        for key, value in inputted_settings.items():
            if isinstance(value, dict):
                flatten_sub_settings = self.get_flatten_settings(value, key)
                flatten_settings.update(
                    {
                        get_cur_key(flatten_key): flatten_value
                        for flatten_key, flatten_value in flatten_sub_settings.items()
                    }
                )
            else:
                flatten_settings[get_cur_key(key)] = value
        return flatten_settings

    def get_django_blueapps_settings(self):
        """获取分散配置在settings中配置项"""
        django_setting_keys = [
            key
            for key in dir(settings)
            if (
                key.startswith(f"{self.SETTING_PREFIX}{self.NESTING_SEPARATOR}")
                or key in BLUEAPPS_SUPPORT_DJANGO_SETTINGS
            )
        ]
        prefix_len = len(f"{self.SETTING_PREFIX}{self.NESTING_SEPARATOR}")
        return {
            key if key in BLUEAPPS_SUPPORT_DJANGO_SETTINGS else key[prefix_len:]: getattr(settings, key)
            for key in django_setting_keys
        }


blueapps_settings = BlueappsSettings(DEFAULT_SETTINGS, IMPORT_SETTINGS)
