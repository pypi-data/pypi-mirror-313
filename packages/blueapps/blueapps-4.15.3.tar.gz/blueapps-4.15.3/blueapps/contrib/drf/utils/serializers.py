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
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DrfValidationError
from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import model_meta

from blueapps.contrib.drf.serializer import format_serializer_errors
from blueapps.contrib.drf.utils.serializer_fields import CustomDateTimeField
from blueapps.core.exceptions import ParamValidationError
from blueapps.utils.db import MultiStrSplitCharField, MultiStrSplitTextField

"""
DRF 常用序列化器
"""


class GeneralSerializer(ModelSerializer):
    """
    自定义ModelSerializer序列化器
    """

    def __init__(self, instance=None, data=empty, **kwargs):
        self.serializer_field_mapping[models.DateTimeField] = CustomDateTimeField
        self.serializer_field_mapping[MultiStrSplitCharField] = serializers.ListField
        self.serializer_field_mapping[MultiStrSplitTextField] = serializers.ListField
        super(GeneralSerializer, self).__init__(instance=instance, data=data, **kwargs)

    def is_valid(self, raise_exception=False):
        """
        参数校验 返回为处理后的异常信息
        """
        try:
            super(GeneralSerializer, self).is_valid(raise_exception)
        # 捕获原生的参数校验异常，抛出SaaS封装的参数校验异常
        except DrfValidationError:
            if self._errors and raise_exception:
                raise ParamValidationError(
                    format_serializer_errors(self.errors, self.fields, self.initial_data),
                )

        return not bool(self._errors)

    def create(self, validated_data):
        """
        序列化器创建数据
        """
        model_class = self.Meta.model

        info = model_meta.get_field_info(model_class)
        many_to_many = {}
        for field_name, relation_info in list(info.relations.items()):
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = model_class.objects.create(**validated_data)
        except TypeError as exc:
            msg = (
                "Got a `TypeError` when calling `%s.objects.create()`. "
                "This may be because you have a writable field on the "
                "serializer class that is not a valid argument to "
                "`%s.objects.create()`. You may need to make the field "
                "read-only, or override the %s.create() method to handle "
                "this correctly.\nOriginal exception text was: %s."
                % (
                    model_class.__name__,
                    model_class.__name__,
                    self.__class__.__name__,
                    exc,
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in list(many_to_many.items()):
                setattr(instance, field_name, value)

        return instance

    class Meta:
        """
        元数据定义
        """

        model = None


class PageSerializer(serializers.Serializer):
    """
    分页序列化器
    """

    page = serializers.IntegerField(help_text=_("页数"))
    pagesize = serializers.IntegerField(help_text=_("每页数量"))


class OrderingSerializer(serializers.Serializer):
    """
    排序序列化器
    """

    ordering = serializers.CharField(help_text=_("排序字段，`-`表示逆序，多个排序字段以`,`分隔"), required=False)


class SearchSerializer(serializers.Serializer):
    """
    关键字序列化器
    """

    search = serializers.CharField(help_text=_("模糊查找，多个查找关键字以`,`分隔"), required=False)


class PostFilterSerializer(serializers.Serializer):
    """
    ORM condition查询序列化器
    example:
    {
        "conditions": [
            {
                "fields": ["name"],
                "operator": "in",
                "values": ["user1", "user2"]
            }
        ]
    }
    """

    class ConditionSerializer(serializers.Serializer):
        """
        单个查询条件序列化器
        """

        fields = serializers.ListField(help_text=_("查询目标字段列表"), child=serializers.CharField(), min_length=1)
        operator = serializers.CharField(help_text=_("查询类型，可选：`in` `contains` `range` `gt(lt)` `gte(lte)..."))
        values = serializers.ListField(help_text=_("查询目标值列表"), min_length=1)

    conditions = serializers.ListField(help_text=_("查询条件"), child=ConditionSerializer(), required=False, default=[])
