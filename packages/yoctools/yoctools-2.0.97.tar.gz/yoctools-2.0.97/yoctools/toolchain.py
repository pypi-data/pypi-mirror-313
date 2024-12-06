# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
import errno

import os
import stat
import tarfile
import subprocess
import platform
import codecs
import shutil

from .tools import *


toolchain_url_64 = "http://yoctools.oss-cn-beijing.aliyuncs.com/csky-elfabiv2-tools-x86_64-minilibc.tar.gz"
toolchain_url_32 = "http://yoctools.oss-cn-beijing.aliyuncs.com/csky-elfabiv2-tools-i386-minilibc.tar.gz"

rsicv_url_64 = 'http://yoctools.oss-cn-beijing.aliyuncs.com/riscv64-elf-x86_64.tar.gz'
rsicv_url_32 = 'http://yoctools.oss-cn-beijing.aliyuncs.com/riscv64-elf-i386.tar.gz'

arm_url_64 = 'http://yoctools.oss-cn-beijing.aliyuncs.com/gcc-arm-none-eabi-x86_64-linux.tar.gz'
arm_url_32 = ''

all_toolchain_url = {
    'csky-abiv2-elf': [toolchain_url_32, toolchain_url_64],
    'riscv64-unknown-elf': [rsicv_url_32, rsicv_url_64],
    'arm-none-eabi': [arm_url_32, arm_url_64]
}


class ToolchainYoC:
    def __init__(self):
        if os.getuid() != 0:
            self.basepath = home_path('.thead')
        else:
            self.basepath = '/usr/local/thead/'


    def download(self, arch):
        toolchain_path = os.path.join(self.basepath, arch)
        if os.path.exists(toolchain_path):
            put_string("Please delete %s first.", toolchain_path, level='error')
            return
        if arch not in all_toolchain_url:
            put_string("Can't find %s from server.", arch, level='error')
            return

        architecture = platform.architecture()
        if architecture[0] == '64bit':
            toolchain_url = all_toolchain_url[arch][1]
        else:
            toolchain_url = all_toolchain_url[arch][0]

        tar_path = '/tmp/' + os.path.basename(toolchain_url)
        if not toolchain_url:
            put_string("Url is empty!", level='error')
            return
        put_string("Start to download toolchain: %s" % arch)
        try:
            wget(toolchain_url, tar_path)
        except Exception as ex:
            put_string(str(ex), level='error')
            put_string("Please ensure that your machine connected to the Internet.", level='info')
            return

        put_string("")
        put_string("Start install, wait half a minute please.")
        if tar_path.endswith('.bz2'):
            with tarfile.open(tar_path, 'r:bz2') as tar:
                tar.extractall(toolchain_path)
        elif tar_path.endswith('.gz'):
            with tarfile.open(tar_path, 'r:gz') as tar:
                tar.extractall(toolchain_path)
        else:
            put_string("%s extra not support." % tar_path, level='error')
            return

        os.remove(tar_path)
        if os.getuid() == 0:
            self.link_bin(toolchain_path)
        else:
            self.update_env(arch)
        put_string("Congratulations! Install the toolchains at `%s`" % toolchain_path)

    def link_bin(self, toolchain_path):
        toolchain_bin = os.path.join(toolchain_path, 'bin')
        files = os.listdir(toolchain_bin)

        for fil in files:
            p = os.path.join(toolchain_bin, fil)
            if os.path.isfile(p):
                if os.stat(p).st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) != 0:
                    linkname = os.path.join('/usr/bin', os.path.basename(p))
                    try:
                        os.symlink(p, linkname)
                    except OSError as e:
                        if e.errno == errno.EEXIST:
                            os.remove(linkname)
                            os.symlink(p, linkname)
                        elif e.errno == errno.EPERM:
                            put_string("Please use: sudo", ' '.join(sys.argv), level='error')
                            exit(-1)
                        else:
                            pass

    def update_env(self, arch):
        toolchain_path = '$HOME/.thead/%s/bin' % arch
        shell = os.getenv('SHELL')
        shell = os.path.basename(shell)

        if shell == 'zsh':
            rc = home_path('.zshrc')

        elif shell == 'bash':
            rc = home_path('.bashrc')

        with codecs.open(rc, 'r', 'UTF-8') as f:
            contents = f.readlines()

        export_path = ''
        for i in range(len(contents)):
            c = contents[i]
            idx = c.find(' PATH')
            if idx > 0:
                idx = c.find('=')
                if idx >= 0:
                    export_path = c[idx + 1:]

                    if export_path.find(toolchain_path) < 0:
                        export_path = 'export PATH=' + toolchain_path + ':' + export_path
                        contents[i] = export_path

        if not export_path:
            contents.insert(0, 'export PATH=' + toolchain_path + ':$PATH\n\n')

        with codecs.open(rc, 'w', 'UTF-8') as f:
            contents = f.writelines(contents)

    def check_toolchain(self, arch='csky-abiv2-elf', verbose=0, force=False):
        bin_file = self.check_program(arch)
        if bin_file == '' or force:
            if force:
                toolchain_path = os.path.join(self.basepath, arch)
                if os.path.exists(toolchain_path):
                    shutil.rmtree(toolchain_path)
            if arch == 'llvm':
                put_string('please install the llvm toolchain first.')
                exit(-1)
            else:
                self.download(arch)
            bin_file = self.check_program(arch)
        else:
            if verbose == 1:
                if os.getuid() == 0:
                    put_string('warn: the toolchains was installed already, link bin file at %s, path = %s.' % (bin_file, os.path.join(self.basepath, arch)), level='warning')
                else:
                    put_string('warn: the toolchains was installed already, path = %s.' % bin_file, level='warning')
        return bin_file

    def which(self, cmd):
        gcc = subprocess.Popen('which ' + cmd, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = gcc.stdout.readlines()
        for text in lines:
            text = text.decode().strip()
            info = 'which: no ' + os.path.basename(cmd) + ' in'
            if not text.find(info) >= 0:
                return text
        return ''

    def check_program(self, arch='csky-abiv2-elf'):
        if arch == 'llvm':
            path = self.which('clang')
        else:
            path = self.which(arch + '-gcc')
        if path == '':
            path = home_path('.thead/' + arch + '/bin/' + arch + '-gcc')
            path = self.which(path)
            return path
        else:
            return path
