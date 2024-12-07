# Seatools-starter-django

seatools ioc 的 django 启动器

## 仓库地址:
1. https://github.com/seatools-py/seatools-starter-django
2. https://gitee.com/seatools-py/seatools-starter-django

## 使用指南
1. 安装, `poetry add seatools-starter-django`
2. 配置`config/application.yml`
```yaml
seatools:
  django:
    # django settings.py 包路径
    settings: xxx.settings
```
2. 使用
```python
from seatools.ioc import run

# 启动ioc
run(scan_package_names=['seatools.ioc.starters.django'])

# 可直接使用django能力包含不限于django-orm等

```
