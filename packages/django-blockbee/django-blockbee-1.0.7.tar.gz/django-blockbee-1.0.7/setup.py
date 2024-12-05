#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-blockbee',
    version='1.0.7',
    packages=find_packages(),
    author="BlockBee",
    author_email="info@blockbee.io",
    install_requires=[
        'django',
        'requests',
    ],
    description="Django implementation of BlockBee's payment gateway",
    long_description_content_type="text/markdown",
    long_description=long_description,
    include_package_data=True,
    url='https://github.com/blockbee-io/django-blockbee',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
    zip_safe=False,
)
