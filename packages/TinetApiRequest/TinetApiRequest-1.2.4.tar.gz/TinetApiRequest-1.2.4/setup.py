from pathlib import Path
from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

# Define our package
setup(
    name="TinetApiRequest",
    version="1.2.4",
    description="天润接口测试库",
    author="天润-测试",
    author_email="zhupeng@ti-net.com.cn",
    url="https://www.ti-net.com.cn/",
    python_requires=">=3.7",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    license='MIT',
)
# python setup.py sdist bdist_wheel
# twine upload dist/*
# zhupengtinet
# 账号: __token__
# 密码: pypi-AgEIcHlwaS5vcmcCJDE5ZGVjOTc0LWY1YjctNGVhMi05OWFlLWZhNzFhYWI1MDcyOQACKlszLCI0NTIzNzJkYi0xNzEyLTQ2YjUtYTBmZi1jYTM0ZTQxNGViMjIiXQAABiD0abj-vqlyLS22IMYQiVOPkRtCk19oCyRdMuUXS2ahiw
# 账号 zp
# pypi-AgEIcHlwaS5vcmcCJGU3NThhZGNiLTlhZmItNGQ4OC1hNmRiLWMzNTgwMDM0ZGZjNgACKlszLCI0NTIzNzJkYi0xNzEyLTQ2YjUtYTBmZi1jYTM0ZTQxNGViMjIiXQAABiA-VFBYRmrG-lcYgoo-rR2zXIfYqSRyNlYY6GxMm6Vhhw
# [pypi]
#   username = __token__
#   password = pypi-AgEIcHlwaS5vcmcCJGZiNGZiMjVlLTk0YTgtNGEyZS1iZTQ3LWQ2MjhmZmVlNTg3ZAACKlszLCI0NTIzNzJkYi0xNzEyLTQ2YjUtYTBmZi1jYTM0ZTQxNGViMjIiXQAABiDKrO1hnxV3RBZvzZhGREgDPkZfEut6DnsAhdjWmZnIvA
#   pypi-AgEIcHlwaS5vcmcCJDE5ZGVjOTc0LWY1YjctNGVhMi05OWFlLWZhNzFhYWI1MDcyOQACKlszLCI0NTIzNzJkYi0xNzEyLTQ2YjUtYTBmZi1jYTM0ZTQxNGViMjIiXQAABiD0abj-vqlyLS22IMYQiVOPkRtCk19oCyRdMuUXS2ahiw
# safeCode
# PyPI recovery codes
# 7dc78210b25a85ce
# 354fd734f3cec93c
# 053c971d923a28e0
# 62ad3ac15c089920
# 78ec32d80ce37a9c
# 05ca7615d3a2192f
# 117c2bab077b6cd0
# 8840385f2976feb9
