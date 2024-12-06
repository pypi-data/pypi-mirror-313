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
import hashlib
import traceback
from collections import namedtuple
from contextlib import contextmanager

from blueapps.utils.logger import logger


@contextmanager
def ignored(*exceptions, **kwargs):
    """
    在忽略某异常下执行
    example:
        with ignored(Exception):
            # 不会抛出异常
            print(1/0)
    """
    try:
        yield
    except exceptions:
        if kwargs.get("log_exception", True):
            logger.warning(traceback.format_exc())


def dict_to_namedtuple(dic):
    """
    从dict转换到namedtuple
    """
    return namedtuple("AttrStore", list(dic.keys()))(**dic)


def choices_to_namedtuple(choices):
    """
    从django-model的choices转换到namedtuple
    """
    return dict_to_namedtuple(dict(choices))


def tuple_choices(tupl):
    """
    从django-model的choices转换到namedtuple
    """
    return [(t, t) for t in tupl]


def md5_sum(src_str: str):
    """
    计算md5_sum值
    @param src_str {str} 源字符串
    """
    md5 = hashlib.md5()
    md5.update(src_str.encode("utf-8"))
    md5_key = md5.hexdigest()
    return md5_key
