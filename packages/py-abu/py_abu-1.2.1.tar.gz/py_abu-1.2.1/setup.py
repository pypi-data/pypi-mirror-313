# -*- coding: utf-8 -*-
# @Time    : 2024/8/7 18:36
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup, find_packages

setup(
    name='py-abu',
    version='1.2.1',
    description='abu API',
    long_description='Private API for abu',
    author='Chris',
    author_email='10512@qq.com',
    url='https://github.com/ChrisYP/abu',
    license='MIT',
    packages=find_packages(),
    package_dir={'py-abu': 'abu'},
    install_requires=["loguru", "pyperclip", "requests", "aiohttp", "Brotli"],
    platforms=["all"],
    include_package_data=True,
    zip_safe=False,
    keywords='abu',
)
