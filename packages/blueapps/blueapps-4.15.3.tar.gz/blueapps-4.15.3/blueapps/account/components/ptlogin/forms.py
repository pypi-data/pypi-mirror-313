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


class AuthenticationForm(forms.Form):
    p_uin = forms.CharField()
    p_skey = forms.CharField()

    def clean(self):
        cleaned_data = {}
        for field_name, value in self.cleaned_data.items():
            if field_name.startswith("p_"):
                field_name = field_name[2:]
            cleaned_data[field_name] = str(value)

        self.cleaned_data.update(cleaned_data)
        return self.cleaned_data

    def clean_p_uin(self):
        p_uin = self.cleaned_data.get("p_uin", "")
        # noinspection PyBroadException
        try:
            return str(int(p_uin[1:]))
        except Exception:  # pylint: disable=broad-except
            raise forms.ValidationError("invalid p_uin")
