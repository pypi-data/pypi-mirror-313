import os
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand
from blueapps.apigw_sync.apigw_sync_settings import apigw_settings


class Command(BaseCommand):
    help = 'Generate apigw definition'

    def add_arguments(self, parser):
        parser.add_argument('--target_dir', type=str, help='Target path for the output file')

    def handle(self, *args, **options):
        # 获取模板文件输出根目录相对路径
        target_dir = options['target_dir'] if options['target_dir'] \
            else apigw_settings.GENERATE_APIGW_DEFINITION_TARGET_DIR
        # 获取模板文件名
        definition_file_name = apigw_settings.APIGW_DEFINITION_FILE_NAME
        # 获取模板文件
        curent_dir = os.path.dirname(os.path.abspath(__file__))
        source_file = os.path.join(curent_dir, 'data', definition_file_name)
        # 获取模板文件输出绝对路径
        target_dir = os.path.join(settings.BASE_DIR, target_dir.strip('/'))
        os.makedirs(target_dir, exist_ok=True)

        target_file = os.path.join(target_dir, definition_file_name)
        if os.path.exists(target_file):
            self.stdout.write(
                self.style.ERROR(
                    f'generate apigw definition template file to {target_file} failed: file already exists'))
            return

        shutil.copy(source_file, target_file)
        self.stdout.write(self.style.SUCCESS(f'Successfully generate apigw definition template file to {target_file}'))
