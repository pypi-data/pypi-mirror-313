# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='zack_liu_package2',  # 包名
    version='1.1.1',  # 版本号
    description='zack_liu_package',
    long_description=long_description,
    author='zack_liu',
    author_email='liu.zhimin.2019@gmail.com',
    url='https://github.com/liuzhimin2019/soho-ui.git',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
)
