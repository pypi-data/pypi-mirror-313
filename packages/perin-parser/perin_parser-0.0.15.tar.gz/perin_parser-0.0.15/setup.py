# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2019-12-28 19:26
from os.path import abspath, join, dirname
from setuptools import find_packages, setup

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='perin_parser',
    version='0.0.15',
    description='(Unofficial) PERIN: Permutation-invariant Semantic Parsing',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ufal/perin',
    author='David Samuel & Milan Straka',
    license='Mozilla Public License 2.0',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        "Development Status :: 3 - Alpha",
        'Operating System :: OS Independent',
        "License :: OSI Approved :: Apache Software License",
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        "Topic :: Text Processing :: Linguistic"
    ],
    keywords='corpus,machine-learning,NLU,NLP',
    packages=find_packages(exclude=['tests', 'scripts', 'data']),
    include_package_data=False,
    install_requires=[
        'scipy',
    ],
    python_requires='>=3.6',
)
