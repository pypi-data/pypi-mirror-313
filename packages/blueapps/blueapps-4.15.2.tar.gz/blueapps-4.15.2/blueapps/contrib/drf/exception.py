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
import json
from json.decoder import JSONDecodeError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from blueapps.core.exceptions import BlueException
from blueapps.utils.logger import logger


def custom_exception_handler(exc, context):
    """
    分类：
        APIException及子类异常
        app自定义异常和未处理异常
    """
    response = exception_handler(exc, context)
    if response:
        return Response(
            response.data["detail"] if "detail" in response.data else response.data, status=response.status_code,
        )

    exc_message = str(exc)
    exc_data = None
    if hasattr(exc, "data") and exc.data:
        try:
            exc_data = json.loads(exc.data)
        except JSONDecodeError:
            exc_data = exc.data
        except TypeError:
            # 其它内容不能被json解析 忽略
            pass

    if hasattr(exc, "message") and exc.message:
        try:
            exc_message = json.loads(str(exc.message))
        except JSONDecodeError:
            exc_message = str(exc.message)

    code = status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    if isinstance(exc, BlueException):
        code = exc.code
        status_code = exc.STATUS_CODE

    data = {
        "code":  code,
        "message": exc_message,
        "data": exc_data,
    }
    # 使用json方便提取
    logger.exception(json.dumps({"code": data["code"], "message": data["message"], "data": data["data"]}))
    return Response(data, status=status_code)
