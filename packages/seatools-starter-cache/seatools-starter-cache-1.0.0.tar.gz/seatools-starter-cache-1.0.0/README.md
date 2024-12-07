# Seatools-starter-cache

seatools ioc 的 cache 启动器

## 仓库地址:
1. https://github.com/seatools-py/seatools-starter-cache
2. https://gitee.com/seatools-py/seatools-starter-cache

## 使用指南
1. 安装, `poetry add seatools-starter-cache`
2. 配置文件`config/application.yml`配置如下
```yaml
# 数据库配置
seatools:
  cache:
    # 缓存的驱动, 默认内置基于内存的驱动：FIFOCache, LFUCache, LRUCache, MRUCache, RRCache, TTLCache, TLRUCache, 支持自定义缓存及配置示例: seatools.cache.ext.SqliteCache
    # 这里以TTLCache为例, 内置驱动均在seatools.cache包下, 可查看具体类型了解驱动参数
    driver: TTLCache
    # 驱动配置
    config:
      maxsize: 100
      ttl: 60

```
3. 使用示例
```python
import cachetools
from seatools.ioc import run, Autowired
from seatools.cache import Cache

# 启动ioc
run(scan_package_names=['seatools.ioc.starters.cache'], config='./config')

# 获取cachetools.Cache容器对象
origin_cache = Autowired(cls=cachetools.Cache)

# 使用seatools Cache工具
cache = Cache(cache=Autowired(cls=cachetools.Cache), debug=True)

# 直接使用cache工具
cache.put('xxx', "xxx") # 存入缓存
cache.get('xxx', default=None) # 取出缓存
cache.evict('xxx', default=None) # 取出并清除缓存

# 使用cache工具装饰器

@cache.cacheable('xxx_${xx}') #  将函数结果存入缓存中, 每次调用优先检查缓存是否存在 , 与cache.get类似, ${} 用于动态渲染参数生成动态配置名称
def get_xxx(xx: str):
    return xx + '123'

@cache.cache_put('xxx_${xx}') # 覆盖缓存
def add_xxx(xx: str, **kwargs):
    ...

@cache.cache_evict('xxx_${xx}') # 删除缓存
def delete_xxx(xx: str):
    ...

```
