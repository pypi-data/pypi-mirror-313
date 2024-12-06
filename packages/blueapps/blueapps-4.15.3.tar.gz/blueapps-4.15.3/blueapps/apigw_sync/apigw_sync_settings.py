import datetime
from django.conf import settings
import json
import os

# 网关相关默认配置项
APIGW_DEFAULT_SETTINGS = {
    # 发布时间，与发布版本拼接成，确保每一次发布都可以重新发布网关资源
    "DEPLOY_DATETIME": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
    # 发布版本 默认为1.0.0
    "RELEASE_VERSION": "1.0.0",
    # 网关所有者
    "MAINTAINERS": ["admin"],
    # 应用申请指定网关所有资源的权限 默认不需要
    "BK_APIGW_APPLY_API_NAME": [],
    # apigw_definition 模板默认输出位置
    "GENERATE_APIGW_DEFINITION_TARGET_DIR": "",
    # apigw_definition_file 模板文件名
    "APIGW_DEFINITION_FILE_NAME": "apigw-definition.yml",
    # api_resources 模板默认输出位置
    "GENERATE_API_RESOURCES_TARGET_DIR": "",
    # api_resources 模板文件名
    "API_RESOURCES_FILE_NAME": "api-resources.yml",
    # SaaS生产环境后端地址
    "BK_APIGW_API_PROD_HOST": os.getenv("BK_APIGW_API_PROD_HOST") or json.loads(
        os.getenv("BKPAAS_DEFAULT_PREALLOCATED_URLS", "{}")).get(
        "prod"),
    # 应用在SaaS部署后默认的预发布环境
    "BK_APIGW_API_STAG_HOST": os.getenv("BK_APIGW_API_STAG_HOST") or json.loads(
        os.getenv("BKPAAS_DEFAULT_PREALLOCATED_URLS", "{}")).get(
        "stag"),
}


class APIGWSettings:
    def __init__(self):
        # 默认网关配置项
        self.apigw_settings = APIGW_DEFAULT_SETTINGS
        # 对配置项进行补充
        self.get_delay_settings()
        # 获取用户定义的网关配置项
        self.user_settings = getattr(settings, "APIGW_DEFINITION_SETTINGS", {})
        # 合并配置项,以用户配置为主
        self.apigw_settings.update(self.user_settings)
        # apigw-manager解析配置文件需要使用settings，进行配置回写
        setattr(settings, "APIGW_DEFINITION_SETTINGS", self.apigw_settings)

    def __getattr__(self, key):
        if key not in self.apigw_settings:
            raise AttributeError
        value = self.apigw_settings[key]
        return value

    def get_delay_settings(self):
        """需要settings加载完毕后进行获取的配置项"""
        # 网关名称 默认为app code 不能有下划线
        self.apigw_settings["BK_APIGW_NAME"] = settings.APP_CODE
        # 网关主动授权给应用，添加访问网关所有资源的权限，默认授权当前saas
        self.apigw_settings["BK_APIGW_GRANT_APPS"] = [settings.APP_CODE, ]


apigw_settings = APIGWSettings()
