from distutils.core import setup

from setuptools import find_packages

setup(name="xbase_util",
      version="0.3.1",
      description="网络安全基础工具",
      long_description="包含提取，预测，训练的基础工具",
      author="xyt",
      author_email="2506564278@qq.com",
      license="<MIT License>",
      packages=find_packages(),
      url="https://gitee.com/jimonik/xbase_util.git",
      install_requires=[
      ],
      zip_safe=False,
      package_data={
            'xbase_util': ['../xbase_util_assets/*'],
      },
      include_package_data=True)
