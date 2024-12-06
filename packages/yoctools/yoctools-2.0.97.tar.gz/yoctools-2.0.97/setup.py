#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.command.build_ext import build_ext as _build_ext
from distutils.core import Extension
import os, stat
import sys
import platform
from codecs import open  # To use a consistent encoding

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

def product_install_process(install_userbase, install_base):
    def _productfile(product_pre):
        architecture = platform.architecture()
        if architecture[0] == '64bit':
            product = os.path.join(product_pre, 'product64')
        else:
            product = os.path.join(product_pre, 'product32')
        return product

    product_prefix = '/usr/local/bin'
    if not os.access('/usr/local/bin', os.W_OK):
        product_prefix = os.path.join(install_base, 'bin')
        if not os.path.isfile(_productfile(product_prefix)):
            product_prefix = os.path.join(install_userbase, 'bin')

    product = _productfile(product_prefix)

    try:
        os.chmod(product, stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except:
        pass

    try:
        os.symlink(product, os.path.join(product_prefix, 'product'))
    except:
        pass

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        product_install_process(self.install_userbase, self.install_base)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        product_install_process(self.install_userbase, self.install_base)


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

APP_NAME = 'yoctools'

RUAMEL_REQ = 'ruamel.yaml==0.15.100'
SCONS_REQ = 'scons>=3.0.0, <4.0.0'
if sys.version_info.major > 2:
    RUAMEL_REQ = 'ruamel.yaml==0.16.13'
    if sys.version_info.minor >= 12:
        SCONS_REQ = 'scons==4.8.0'

settings = dict()

settings.update(
    name=APP_NAME,
    version=get_version("yoctools/cmd.py"),
    description='YoC tools',
    author='Zhuzhg',
    author_email='zzg@ifnfn.com',
    packages=find_packages(),
    # packages = ['yoctools', 'git', 'gitdb', 'yaml'],
    install_requires=[
        'import-scons>=2.0.0',
        SCONS_REQ,
        'requests_toolbelt',
        'threadpool',
        'smmap',
        'configparser==4.0.2',
        RUAMEL_REQ,
        'pyserial',
        'xlsxwriter'
    ],

    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    data_files=[
        ('bin', ['yoctools/build/product64']),
        ('bin', ['yoctools/build/product32']),
        ('bin', ['yoctools/build/gen_ldfile.sh']),
        ('lib/yoctools/script', [
            'yoctools/script/after_build.sh',
            'yoctools/script/gdbinit',
            'yoctools/script/flash.init',
            'yoctools/script/before_build.sh',
            'yoctools/script/README.md',
        ]),
    ],
    entry_points={
        'console_scripts': [
            'yoc = yoctools.cmd:main',
            'cct = yoctools.cmd:cct_main'
        ],
    },
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
)


setup(**settings)
