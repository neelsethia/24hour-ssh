#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import io
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Load the package's __init__.py module as a dictionary.
about = {}
with open(os.path.join(here, 'ec2ssh/__init__.py')) as f:
    exec(f.read(), about)

setup(
    name='24hour-ssh',
    #version=about['__version__'],
    version='0.0.0',
    description='Safely provide temporary ssh access to AWS EC2 instances',
    long_description=long_description,
    url='https://github.com/ucop-tds/24hour-ssh',
    keywords='aws ec2 ssm ssh boto3',
    author=['Ashley Gould', 'Neel Sethia'],
    author_email=['agould@ucop.edu', 'neel.sethia@ucop.edu'],
    license='GPLv3',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'botocore',
        'boto3',
        'awscli',
        'PyYAML',
    ],
    test_requires=[
        'moto',
        'pytest',
        'flake8',
    ],
    packages=find_packages(
        '.',
        exclude=[
            'tests',
            'cfn',
        ],
    ),
    include_package_data=True,
    zip_safe=False,
)

