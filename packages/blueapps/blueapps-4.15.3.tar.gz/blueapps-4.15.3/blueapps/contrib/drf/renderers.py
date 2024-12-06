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
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.status import is_success

from blueapps.utils.request_provider import get_or_create_local_request_id


class APIRenderer(JSONRenderer):
    """
    统一的结构封装返回内容
    """

    SUCCESS_CODE = 0

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        统一处理返回数据
        """
        response = renderer_context["response"]
        req_id = get_or_create_local_request_id()

        res_data = {
            "result": True,
            "code": self.SUCCESS_CODE,
            "data": None,
            "message": None,
            "request_id": req_id,
            "trace_id": getattr(renderer_context.get("request"), "otel_trace_id", None),
        }

        if is_success(response.status_code):
            response.status_code = status.HTTP_200_OK
            res_data["data"] = data
            res_data["code"] = self.SUCCESS_CODE
            return super(APIRenderer, self).render(res_data, accepted_media_type, renderer_context)

        code = response.status_code
        message = response.data
        errors = response.data
        if isinstance(response.data, dict) and "code" in response.data:
            code = response.data["code"]
            message = self.pretty_dict(response.data["message"])
            errors = response.data["data"]

        res_data.update({"result": False, "code": code, "message": message, "errors": errors})

        return super(APIRenderer, self).render(res_data, accepted_media_type, renderer_context)

    def pretty_dict(self, dict_data):  # pylint: disable=no-self-use
        """
        将字典转为字符串返回
        格式: {key}: {value}
        """
        if not isinstance(dict_data, dict) or not dict_data:
            return dict_data
        res = []
        for key, value in dict_data.items():
            res.append(f"{key}: {value}")
        return "; ".join(res)
