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
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from blueapps.core.exceptions import ParamValidationError
from blueapps.utils.time import strftime_local


class MultipleIntField(serializers.Field):
    """
    用于整数多选查询的字段
    """

    def to_internal_value(self, data):  # pylint: disable=no-self-use
        """
        Transform the *incoming* primitive data into a native value.
        """
        ret = []
        for value in data.split(","):
            try:
                ret.append(int(value))
            except ValueError:
                raise ParamValidationError(_("请求参数必须全部为整数"))
        return ret

    def to_representation(self, value):  # pylint: disable=no-self-use
        """
        Transform the *outgoing* native value into primitive data.
        """
        return value


class MultipleStrField(serializers.Field):
    """
    用于字符串多选查询的字段
    """

    def to_internal_value(self, data):  # pylint: disable=no-self-use
        """
        Transform the *incoming* primitive data into a native value.
        """
        data = [str(value) for value in data.split(",")]
        return data

    def to_representation(self, value):  # pylint: disable=no-self-use
        """
        Transform the *outgoing* native value into primitive data.
        """
        return value


class CustomDateTimeField(serializers.DateTimeField):
    """
    自定义数据库时间字段
    """

    def to_representation(self, value):  # pylint: disable=no-self-use
        """
        Transform the *outgoing* native value into primitive data.
        """
        if not value:
            return None

        return strftime_local(
            value,
            fmt=settings.REST_FRAMEWORK.get("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S%z"),
        )
