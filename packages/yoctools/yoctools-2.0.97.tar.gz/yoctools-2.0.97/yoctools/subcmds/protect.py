# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
from yoctools import *


class Protect(Command):
    common = True
    helpSummary = "set branch protection"
    helpUsage = """
%prog
"""
    helpDescription = """
set branch protection
"""

    def _Options(self, p):
        p.add_option('-b', '--branch',
                     dest='branch', action='store', type='string',
                     help='set branch protection')
        p.add_option('-c', '--cancel',
                     dest='cancel', action='store_true',
                     help='cancel branch protection')

    def Execute(self, opt, args):
        if not (opt.branch):
            self.Usage()
            return
        br = opt.branch
        yoc = YoC()
        components = ComponentGroup()
        for component in yoc.components:
            if len(args) > 0:
                if component.name not in args:
                    continue
            if os.path.exists(os.path.join(component.path, '.git')):
                components.add(component)
        if len(components) == 0:
            put_string("There no git repo found in your workspace.", level='error')
            exit(0)
        repo = RepoGitee(yoc.conf.gitee_token, yoc.conf.group)
        count = 0
        for component in components:
            count = count + 1
            if opt.cancel:
                put_string("[%d/%d]Start to cancel branch: %s protection for component: %s ." % (count, len(components), br, component.name))
                repo.delete_branch_protection(component.name, br)
                continue
            put_string("[%d/%d]Start to set branch: %s protection for component: %s ." % (count, len(components), br, component.name))
            repo.set_branch_protection(component.name, br)
