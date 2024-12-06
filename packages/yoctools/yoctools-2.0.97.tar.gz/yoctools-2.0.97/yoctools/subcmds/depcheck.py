# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
from curses import flash

from yoctools import *


class Depcheck(Command):
    common = True
    helpSummary = "Checkout the depends' components' branch of the current solution"
    helpUsage = """
%prog [option]
"""
    helpDescription = """
Checkout the depends' components' branch of the current solution.
"""

    def _Options(self, p):
        p.add_option('-c', '--calibrate',
                     dest='calibrate', action='store_true',
                     help='calibrate the depend components for current solution')
        p.add_option('-b', '--board',
                     dest='board_name', action='store', type='str', default=None,
                     help='specify board name')
        p.add_option('-s', '--sdk',
                     dest='sdk_name', action='store', type='str', default=None,
                     help='specify chip sdk name')

    def Execute(self, opt, args):
        yoc = YoC()
        not_filter = not (opt.board_name or opt.sdk_name)
        solution = yoc.getSolution(board_name=opt.board_name, sdk_name=opt.sdk_name, not_filter=not_filter, file_non_existent_no_err=True)
        if solution == None:
            put_string("The current directory is not a solution!", level='error')
            exit(0)
        flag = False
        for c in solution.components:
            git = GitRepo(c.path, c.repo_url)
            ab, _ = git.safe_active_branch()
            # print(c.name, c.version, ab, c.depends)
            if str(c.version) != str(ab):
                put_string("The %s' version(%s) and actived barnch(%s) is not matched!" % (c.name, c.version, ab), level='warning')
                flag = True
            for item in c.depends:
                cname = list(item.keys())[0]
                cver = list(item.values())[0]
                # print(cname, cver)
                for comp in solution.components:
                    if cname == comp.name and cver != comp.version:
                        if opt.calibrate:
                            put_string("The needed version(%s) and version(%s) for %s is not matched! Calibrate now." % (cver, comp.version, cname), level='warning')
                            git = GitRepo(comp.path, comp.repo_url)
                            git.CheckoutBranch(cver)
                        else:
                            put_string("The needed version(%s) and version(%s) for %s is not matched!" % (cver, comp.version, cname), level='warning')
                        flag = True
        if not flag:
            put_string("Everything seems to be ok.")
