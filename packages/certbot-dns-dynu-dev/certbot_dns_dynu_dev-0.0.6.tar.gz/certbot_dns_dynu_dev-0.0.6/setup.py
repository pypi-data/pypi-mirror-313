#! /usr/bin/env python
"""Test for DNS Authenticator for Dynu"""

from os import path
from setuptools import setup
from setuptools import find_packages

VERSION = "0.0.6"

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'acme>=2.0.0',
    'certbot>=2.0.0',
    'dns-lexicon>=3.11.7',
    'tldextract==5.1.2; python_version == "3.8"',
    'dnspython',
    'mock',
    'setuptools',
    'requests'
]


here = path.abspath(path.dirname(__file__))

setup(
    name='certbot-dns-dynu-dev',
    version=VERSION,

    description="Dynu DNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BigThunderSR/certbot-dns-dynu-dev',
    download_url='https://github.com/BigThunderSR/certbot-dns-dynu-dev/archive/refs/tags/'
                + VERSION + '.tar.gz',
    author="Bikramjeet Sing, updated by BigThunderSR",
    license='Apache License 2.0',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(),
    install_requires=install_requires,

    # extras_require={
    #     'docs': docs_extras,
    # },

    entry_points={
        'certbot.plugins': [
            'dns-dynu = certbot_dns_dynu_dev.dns_dynu:Authenticator',
        ],
    },
    test_suite='certbot_dns_dynu_dev',
)
