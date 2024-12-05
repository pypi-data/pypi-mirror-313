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
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    """
    自定义分页
    """

    # 默认一页拉取的数量
    page_size = 100

    # 获取URL参数中传入的页码key字段
    page_query_param = "page"

    # 指定单页最大值的字段
    page_size_query_param = "page_size"

    # 设置单次拉取的最大值
    max_page_size = 1000

    def get_paginated_response(self, data):
        """
        返回分页后的Response
        """
        return Response(
            OrderedDict(
                [
                    ("page", self.page.number),
                    ("num_pages", self.page.paginator.num_pages),
                    ("total", self.page.paginator.count),
                    ("results", data),
                ]
            )
        )

    def get_paginated_data(self, data):
        """
        生成分页数据
        """
        return OrderedDict(
            [
                ("page", self.page.number),
                ("num_pages", self.page.paginator.num_pages),
                ("total", self.page.paginator.count),
                ("results", data),
            ]
        )
