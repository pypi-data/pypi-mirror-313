#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = open('requirements.txt').readlines()

setup(
    name='messagev',
    version='0.0.27',
    description="MessageV: the python files generated for consuming the OrchestSh API",
    long_description=readme + '\n\n' + history,
    author="Vauxoo",
    author_email='info@vauxoo.com',
    url='',
    packages=[
        'messagev',
    ],
    package_dir={'messagev':
                     'messagev'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='messagev',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
