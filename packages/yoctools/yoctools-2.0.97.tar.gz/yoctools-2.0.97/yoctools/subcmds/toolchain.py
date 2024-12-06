# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

import os
from yoctools import *


class Toolchain(Command):
    common = True
    helpSummary = "Install toolchain"
    helpUsage = """
%prog [--all] [--csky] [--riscv]
"""
    helpDescription = """
Install toolchain.
"""

    def _Options(self, p):
        p.add_option('-f', '--force',
                     dest='force', action='store_true',
                     help=' install toolchain force')
        p.add_option('-c', '--csky',
                     dest='install_csky', action='store_true',
                     help=' install csky-elfabiv2-tools')
        p.add_option('-r', '--riscv',
                     dest='install_riscv', action='store_true',
                     help=' install riscv-elf-tools')
        p.add_option('-a', '--all',
                     dest='install_all', action='store_true',
                     help=' install csky-elfabiv2-tools and riscv-elf-tools')

    def Execute(self, opt, args):
        if os.getuid() != 0:
            put_string(
                'Error: you cannot perform this operation unless you are root. Please input as follow:\nsudo yoc ' + ' '.join(sys.argv[1:]), level='error')
            exit(-1)

        need_usage = True
        tool = ToolchainYoC()
        if opt.install_all:
            tool.check_toolchain('csky-abiv2-elf', 1, force=opt.force)
            tool.check_toolchain('riscv64-unknown-elf', 1, force=opt.force)
            need_usage = False
        else:
            if opt.install_csky:
                tool.check_toolchain('csky-abiv2-elf', 1, force=opt.force)
                need_usage = False
            if opt.install_riscv:
                tool.check_toolchain('riscv64-unknown-elf', 1, force=opt.force)
                need_usage = False
        if need_usage:
            self.Usage()
