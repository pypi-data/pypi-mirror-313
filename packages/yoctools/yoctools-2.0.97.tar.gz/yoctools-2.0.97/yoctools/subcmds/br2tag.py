# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *


class Br2tag(Command):
    common = True
    helpSummary = "Set branch to tag"
    helpUsage = """
%prog [<compnent> ...]
"""
    helpDescription = """
Set branch to tag
"""
    def _Options(self, p):
        p.add_option('-b', '--branch',
                     dest='branch_name', action='store', type='string',
                     help='the branch')
        p.add_option('-t', '--tag',
                     dest='tag_name', action='store', type='string',
                     help='the tag')
    def Execute(self, opt, args):
        if not opt.branch_name or not opt.tag_name:
            return
        yoc = YoC()
        repo = RepoGitee(yoc.conf.gitee_token, yoc.conf.group)
        if len(args) == 0:
            for component in yoc.components:
                repo.branch_to_tag(component.name, opt.branch_name, opt.tag_name)
        else:
            for arg in args:
                component = yoc.components.get(arg)
                if component:
                    repo.branch_to_tag(component.name, opt.branch_name, opt.tag_name)
