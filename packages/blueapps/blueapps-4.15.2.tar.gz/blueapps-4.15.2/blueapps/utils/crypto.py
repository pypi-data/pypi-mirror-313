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
import typing

from django.conf import settings

try:
    from bkcrypto.contrib.django.fields import SymmetricTextField as CustomTextField


except ImportError:
    # 没有 bkcrypto-python-sdk 相关依赖，此时不启用加密
    from django.db import models

    class CustomTextField(models.TextField):
        def __init__(self, *args, using: typing.Optional[str] = None, **kwargs):
            self.using = using or "default"

            super(CustomTextField, self).__init__(*args, **kwargs)


class SymmetricTextField(CustomTextField):
    def get_decrypted_value(self, value):
        if value is None:
            return super().get_decrypted_value(value)
        return super().get_decrypted_value(str(value))

    @property
    def enable_encryption(self) -> bool:
        """
        开发框架是否已指定 cipher 实例对 SymmetricTextField 所涉及的 DB 字段进行加密
        不指定时采取明文落库策略
        """
        return bool(settings.BLUEAPPS_ENABLE_DB_ENCRYPTION)

    def encrypt(self, plaintext: str) -> str:
        if self.enable_encryption:
            return super().encrypt(plaintext)
        return plaintext

    def decrypt(self, ciphertext_with_prefix: str) -> str:
        if self.enable_encryption:
            return super().decrypt(ciphertext_with_prefix)
        return ciphertext_with_prefix
