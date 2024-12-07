# -*- coding: utf-8 -*-
# @Time    : 2024/12/5 4:38 下午
# @Author  : dubaichuan
# @File    :setup.py
# @Software: PyCharm


from setuptools import setup, find_packages

setup(
    name='read_dir',  # 包的名称
    version='1.0.1',  # 包的版本号
    author='skynyx',  # 作者姓名
    description='读取文件',  # 包的描述信息
    packages=find_packages(),  # 包含的子包列表
    install_requires=[
        'pandas>=0.18.0',
        'numpy>=1.9.2'
    ]  # 依赖项列表
)
