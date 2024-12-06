#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='gimoos_ddf',
    version='0.3.7',
    description='极墨思驱动开发框架',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='one-ccs',
    author_email='one-ccs@foxmail.com',
    url='https://github.com/one-ccs/gimoos_ddf',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.10',
    packages=find_packages(),
    package_dir={},
    package_data={},
    exclude_package_data={},
    install_requires=[
        'tqdm',
        'aiohttp',
    ],
    entry_points={
        'console_scripts': [
            'gimoos_ddf = gimoos_ddf.management:execute_from_command_line',
        ],
    },
)
