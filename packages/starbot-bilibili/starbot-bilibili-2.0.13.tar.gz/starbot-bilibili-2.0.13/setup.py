#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_namespace_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='starbot-bilibili',
    version='2.0.13',
    license='GNU Affero General Public License v3.0',
    description='一款极速，多功能的哔哩哔哩推送机器人',
    author='LWR',
    author_email='lwr1104@qq.com',
    url='https://github.com/Starlwr/StarBot',
    packages=find_namespace_packages(),
    package_data={
        'starbot.api': ['*.json'],
        'starbot.resource': ['*.png', '*.ttf']
    },
    install_requires=[
        'Brotli>=1.0.9', 
        'aiomysql>=0.1.1',
        'redis>=4.5.5',
        'emoji>=2.2.0',
        'graia-broadcast==0.19.2',
        'creart==0.2.2',
        'creart-graia==0.1.5',
        'graia-ariadne==0.9.8',
        'graia-saya==0.0.16',
        'jieba>=0.42.1',
        'scipy>=1.10.0',
        'Pillow==9.5.0',
        'numpy==1.24.3',
        'matplotlib==3.7.1',
        'wordcloud>=1.8.2.2'
    ],
    keywords='starbot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.8"
)