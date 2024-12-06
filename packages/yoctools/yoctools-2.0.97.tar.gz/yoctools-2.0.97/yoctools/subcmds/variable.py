# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *


class Variable(Command):
    common = True
    helpSummary = "Display variables for the current solution"
    helpUsage = """
%prog [option] [<variable>...]
"""
    helpDescription = """
Display variables for the current solution
"""
    def _Options(self, p):
        p.add_option('-b', '--board',
                     dest='board_name', action='store', type='str', default=None,
                     help='show all source code file')
        p.add_option('-s', '--sdk',
                     dest='sdk_name', action='store', type='str', default=None,
                     help='specify chip sdk name')

    def Execute(self, opt, args):
        yoc = YoC()
        not_filter = not (opt.board_name or opt.sdk_name)
        solution = yoc.getSolution(board_name=opt.board_name, sdk_name=opt.sdk_name, not_filter=not_filter)
        if solution == None:
            put_string("The current directory is not a solution!", level='error')
            exit(0)
        if len(args) == 0:
            for k, v in solution.variables.items():
                put_string("%-10s = %s" % (k, v))
        else:
            for arg in args:
                var = solution.variables.get(arg)
                put_string(var)
