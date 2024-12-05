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
from rest_framework import filters
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from blueapps.contrib.drf.utils.serializers import GeneralSerializer
from blueapps.contrib.drf.utils.viewset_mixin import ApiMixin, ValidationMixin


class APIViewSet(ApiMixin, ValidationMixin, GenericViewSet):
    """封装 APIViewSet"""


class Meta:
    """Empty object"""

    pass


class GeneralModelViewSet(ApiMixin, ValidationMixin, ModelViewSet):
    """
    DRF 自定义modelViewSet
    """

    model = None
    filter_backends = (
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    serializer_meta = type("Meta", (Meta,), {"model": None, "ref_name": None})

    def __init__(self, *args, **kwargs):
        super(GeneralModelViewSet, self).__init__(**kwargs)
        self.filter_fields = [f.name for f in self.model._meta.get_fields()]
        self.view_set_name = self.get_view_object_name(*args, **kwargs)

    def get_view_name(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Return the view name, as used in OPTIONS responses and in the
        browsable API.
        """
        return self.model._meta.db_table  # pylint: disable=protected-access

    def get_view_description(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Return some descriptive text for the view, as used in OPTIONS responses
        and in the browsable API.
        """
        return self.model._meta.verbose_name  # pylint: disable=protected-access

    def get_view_module(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        获取视图设置的model
        """
        return getattr(self.model._meta, "module", None)  # pylint: disable=protected-access

    def get_view_object_name(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        获取视图设置的model名称
        """
        return getattr(self.model._meta, "object_name", None)  # pylint: disable=protected-access

    def get_queryset(self):
        """
        重写视图类get_queryset方法
        """
        return self.model.objects.all()

    def get_serializer_class(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        获取视图类序列化器
        """
        self.serializer_meta.model = self.model
        self.serializer_meta.fields = "__all__"
        if isinstance(self.serializer_class, GeneralSerializer) or self.serializer_class is None:
            self.serializer_meta.ref_name = self.model.__name__
            return type(
                "GeneralSerializer{}".format(self.model.__name__), (GeneralSerializer,), {"Meta": self.serializer_meta},
            )

        return self.serializer_class
