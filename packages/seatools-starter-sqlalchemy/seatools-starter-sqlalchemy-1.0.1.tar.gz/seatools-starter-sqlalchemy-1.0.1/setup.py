#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = []

with open('requirements.txt', encoding='utf-8') as f:
    for require in f.readlines():
        require = require.strip()
        if require:
            requirements.append(require)

test_requirements = []

setup(
    author="dragons96",
    author_email='521274311@qq.com',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
    ],
    description="seatools ioc sqlalchemy 启动器",
    install_requires=requirements,
    extras_require={},
    license="MIT license",
    long_description='',
    include_package_data=True,
    keywords=['seatools', 'ioc', 'starter', 'sqlalchemy'],
    name='seatools-starter-sqlalchemy',
    packages=find_packages(include=['seatools.ioc.starters', 'seatools.ioc.starters.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitee.com/seatools-py/seatools-starter-sqlalchemy',
    version='1.0.1',
    zip_safe=False,
)
