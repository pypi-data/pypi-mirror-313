import os
from seatools.ioc import Bean
from seatools.ioc.config import cfg
from loguru import logger


@Bean
def init_django():
    config = cfg()
    settings = None
    if 'seatools' in config and 'django' in config['seatools'] and 'settings' in config['seatools']['django']:
        settings = config['seatools']['django']['settings']
    # 兼容旧参数
    elif 'package_name' in config:
        settings = f'{config["package_name"]}.django.settings'
    if not settings:
        logger.warning('配置属性[seatools.django.settings]不存在, 无法自动初始化数django')
        return
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)
    import django
    django.setup()
