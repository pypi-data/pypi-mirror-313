import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from blueapps.apigw_sync.apigw_sync_settings import apigw_settings


class Command(BaseCommand):
    help = 'Sync SaaS API Gateway'

    def add_arguments(self, parser):
        parser.add_argument('--definition_file', type=str, help='The relative path of the definition file')
        parser.add_argument('--resources_file', type=str, help='The relative path of the resources file')

    def handle(self, *args, **options):
        # 获取APP_CODE
        app_code = settings.APP_CODE
        # 获取文件路径
        definition_file = options['definition_file'] if options['definition_file'] \
            else os.path.join(apigw_settings.GENERATE_APIGW_DEFINITION_TARGET_DIR,
                              apigw_settings.APIGW_DEFINITION_FILE_NAME)
        resources_file = options['resources_file'] if options['resources_file'] \
            else os.path.join(apigw_settings.GENERATE_API_RESOURCES_TARGET_DIR,
                              apigw_settings.API_RESOURCES_FILE_NAME)
        # 获取文件绝对路径
        definition_file_path = os.path.join(settings.BASE_DIR, definition_file)
        resources_file_path = os.path.join(settings.BASE_DIR, resources_file)
        api_name = apigw_settings.BK_APIGW_NAME

        # 同步网关基本信息
        call_command("sync_apigw_config", file=definition_file_path, api_name=api_name)
        self.stdout.write(
            self.style.SUCCESS("[%s] Successfully called sync_apigw_config with definition: %s" % (
                app_code, definition_file_path)))

        # 同步网关环境信息
        call_command("sync_apigw_stage", file=definition_file_path, api_name=api_name)
        self.stdout.write(
            self.style.SUCCESS(
                "[%s] Successfully called sync_apigw_stage with definition: %s" % (app_code, definition_file_path)))

        # 同步网关资源 --del
        call_command("sync_apigw_resources", "--delete", file=resources_file_path, api_name=api_name)
        self.stdout.write(
            self.style.SUCCESS("[%s] Successfully called sync_apigw_resources with resources: %s" % (
                app_code, resources_file_path)))

        # 创建资源版本并发布
        call_command("create_version_and_release_apigw", "--generate-sdks", file=definition_file_path,
                     api_name=api_name, stage=[settings.ENVIRONMENT])
        self.stdout.write(self.style.SUCCESS(
            "[%s] Successfully called create_version_and_release_apigw with definition: %s" % (
                app_code, definition_file_path)))

        # 为应用主动授权 可选
        call_command("grant_apigw_permissions", file=definition_file_path, api_name=api_name)
        self.stdout.write(self.style.SUCCESS(
            "[%s] Successfully called grant_apigw_permissions with definition: %s" % (
                app_code, definition_file_path)))

        # 获取网关公钥
        call_command("fetch_apigw_public_key", api_name=api_name)
        self.stdout.write(self.style.SUCCESS("[%s] Successfully called fetch_apigw_public_key" % app_code))
