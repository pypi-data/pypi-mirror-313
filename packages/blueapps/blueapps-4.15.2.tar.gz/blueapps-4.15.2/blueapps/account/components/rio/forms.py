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

from django import forms


class RioAuthenticationForm(forms.Form):

    # RIO请求需要从HTTP头获取
    HTTP_TIMESTAMP = forms.CharField()
    HTTP_SIGNATURE = forms.CharField()
    HTTP_STAFFID = forms.CharField()
    HTTP_STAFFNAME = forms.CharField()
    HTTP_X_EXT_DATA = forms.CharField()
    HTTP_X_RIO_SEQ = forms.CharField()
