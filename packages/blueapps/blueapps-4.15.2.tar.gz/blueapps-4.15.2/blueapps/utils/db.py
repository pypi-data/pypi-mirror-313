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
from django.core import exceptions
from django.db import models

"""
数据库常用工具类
"""


class MultiStrSplitFieldMixin(models.Field):
    """
    多个字段，使用逗号隔开，入库list->str， 出库 str->list
    头尾都加逗号","，为了方便使用ORM的contains进行过滤且避免子集字符串的越权问题
    """

    def read_from_db(
            self, value, expression, connection
    ):  # pylint: disable=unused-argument
        """
        从db读取 -> 转为列表
        """
        if not value:
            return []
        try:
            value = value.split(",")
        except (TypeError, KeyError):
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )
        result = []
        # 去除头尾逗号
        for _v in value[1:-1]:
            try:
                result.append(self.sub_type(_v))
            except ValueError:
                continue

        return result

    def write_to_db(self, value):
        """
        写入db -> 通过,拼街
        """
        if not value:
            return ""

        if isinstance(value, str):
            value = value.split(",")

        value = [str(_value) for _value in value]
        try:
            value = f",{','.join(value)},"
        except (TypeError, KeyError):
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )

        return value


class MultiStrSplitCharField(models.CharField, MultiStrSplitFieldMixin):
    """
    ORM Char字符串列表字段
    """

    def __init__(self, *args, **kwargs):
        self.sub_type = kwargs.get("sub_type") or str
        kwargs.pop("sub_type", "")
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        """
        从DB读取 与MultiStrSplitFieldMixin一致
        """
        return super().read_from_db(value, expression, connection)

    def get_prep_value(self, value):
        """Perform preliminary non-db specific value checks and conversions."""
        return super().write_to_db(value)


class MultiStrSplitTextField(models.TextField, MultiStrSplitFieldMixin):
    """
    ORM Text字符串列表字段
    """

    def __init__(self, *args, **kwargs):
        self.sub_type = kwargs.get("sub_type") or str
        kwargs.pop("sub_type", "")
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        """
        从DB读取 与MultiStrSplitFieldMixin一致
        """
        return super().read_from_db(value, expression, connection)

    def get_prep_value(self, value):
        """Perform preliminary non-db specific value checks and conversions."""
        return super().write_to_db(value)
