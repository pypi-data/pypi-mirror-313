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

# To use a consistent encoding
from codecs import open
from os import path

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
version = __import__("blueapps").__version__

setup(
    name="blueapps",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,
    description="development framework for blueking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="https://github.com/TencentBlueKing/blueapps",
    # Author details
    author="blueking",
    author_email="blueking@tencent.com",
    include_package_data=True,
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "Django>=2.2.6,<5.0.0",
        "bkoauth>=0.0.12",
        "MarkupSafe>=1.1.1,<3.0.0",
        "Mako>=1.0.6,<2.0",
        "requests>=2.22.0,<3.0.0",
        "python-json-logger>=0.1.7",
        "whitenoise>=3.3.0,<7",
        "Werkzeug>=1.0.0,<3.0.0",
        # jwt
        "pyCryptodome>=3.9.7",
        "PyJWT>=1.6.1,<3.0",
        "cryptography>=2.7",
    ],
    extras_require={
        "opentelemetry": [
            "opentelemetry-api>=1.6.2,<2.0.0",
            "opentelemetry-sdk>=1.6.2,<2.0.0",
            "opentelemetry-exporter-otlp>=1.6.2,<2.0.0",
            "opentelemetry-exporter-jaeger>=1.6.2,<2.0.0",
            "opentelemetry-exporter-jaeger-proto-grpc>=1.6.2,<2.0.0",
            "opentelemetry-exporter-jaeger-thrift>=1.6.2,<2.0.0",
            "opentelemetry-instrumentation>=0.25b2,<1.0.0",
            "opentelemetry-instrumentation-celery>=0.25b2,<1.0.0",
            "opentelemetry-instrumentation-django>=0.25b2,<1.0.0",
            "opentelemetry-instrumentation-dbapi>=0.25b2,<1.0.0",
            "opentelemetry-instrumentation-redis>=0.25b2,<1.0.0",
            "opentelemetry-instrumentation-logging>=0.25b2,<1.0.0",
            "opentelemetry-instrumentation-requests>=0.25b2,<1.0.0",
            "prometheus-client>=0.9.0,<1.0.0",
            "django-prometheus>=2.1.0,<3.0.0",
        ],
        "bkcrypto": ["bk-crypto-python-sdk>=1.1.1,<3.0.0"],
        "bk-notice": ["bk-notice-sdk>=1.1.1,<2.0.0"],
        "apigw-manager": ["apigw-manager>=1.1.5,<3.0.0"],
    },
    zip_safe=False,
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={"console_scripts": ["bk-admin=blueapps.contrib.bk_commands:bk_admin"]},
)
