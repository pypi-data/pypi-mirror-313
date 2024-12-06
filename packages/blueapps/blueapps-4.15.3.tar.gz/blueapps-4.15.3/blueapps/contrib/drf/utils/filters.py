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


class GeneralSearchFilter(filters.SearchFilter):
    """
    django filter关键字过滤器
    """

    def get_search_terms(self, request):
        """重写get_search_terms方法，支持非GET方法的模糊查询"""
        if request.method not in ["GET", "DELETE"]:
            request.query_params._mutable = True  # pylint: disable=protected-access
            if not request.query_params.get(self.search_param):
                request.query_params[self.search_param] = request.data.get(self.search_param, "")
            request.query_params._mutable = False  # pylint: disable=protected-access
        return super().get_search_terms(request)


class GeneralOrderingFilter(filters.OrderingFilter):
    """
    django filter排序过滤器
    """

    def get_ordering(self, request, queryset, view):
        """重写get_ordering方法，支持非GET方法的模糊查询"""
        if request.method not in ["GET", "DELETE"]:
            request.query_params._mutable = True  # pylint: disable=protected-access
            if not request.query_params.get(self.ordering_param):
                request.query_params[self.ordering_param] = request.data.get(self.ordering_param)
            request.query_params._mutable = False  # pylint: disable=protected-access
        return super().get_ordering(request, queryset, view)
