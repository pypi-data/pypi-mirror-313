import importlib
from typing import Optional

from seatools.models import BaseModel
from seatools.ioc.config import cfg
from seatools.ioc.injects import Bean
from seatools import cache
from loguru import logger


class CacheConfig(BaseModel):
    driver: Optional[str] = 'FIFOCache'
    config: Optional[dict] = {'maxsize': 100}


@Bean
def init_cache():
    config = cfg()
    cache_config = None
    if 'seatools' in config and 'cache' in config['seatools']:
        cache_config = config['seatools']['cache']
    if not cache_config:
        logger.warning('配置[seatools.cache]不存在, 无法自动初始化cache bean实例')
        return
    if not isinstance(cache_config, dict):
        logger.error('配置[seatools.cache]属性不是字典类型, 无法自动初始化cache bean实例')
        exit(1)

    cache_config = CacheConfig(**cache_config)
    cache_cls = getattr(cache, cache_config.driver, None)
    if not cache_cls:
        driver_module_chunks = cache_config.driver.split('.')
        driver_module_name, driver_cls_name = '.'.join(driver_module_chunks[:-1]), driver_module_chunks[-1]
        driver_module = importlib.import_module(driver_module_name)
        cache_cls = getattr(driver_module, driver_cls_name)

    cache_instance = cache_cls(**cache_config.config)
    Bean(name='cache', primary=True)(cache_instance)
