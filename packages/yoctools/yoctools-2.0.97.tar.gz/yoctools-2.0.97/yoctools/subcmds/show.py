# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *


class Show(Command):
    common = True
    helpSummary = "Display the detailed compilation information of the current solution"
    helpUsage = """
%prog [option]
"""
    helpDescription = """
Display the detailed compilation information of the current solution.
"""

    def _Options(self, p):
        p.add_option('-a', '--all',
                     dest='show_all', action='store_true',
                     help='show the complete list of commands')
        p.add_option('-c', '--show-component',
                     dest='show_component', action='store_true',
                     help='show all component')
        p.add_option('-i', '--show-include',
                     dest='show_include', action='store_true',
                     help='show all include path')
        p.add_option('-l', '--show-libs',
                     dest='show_libs', action='store_true',
                     help='show all libs')
        p.add_option('-f', '--show-flags',
                     dest='show_flags', action='store_true',
                     help='show all FLAGS')
        p.add_option('-v', '--show-variable',
                     dest='show_variables', action='store_true',
                     help='show all variables')
        p.add_option('-d', '--show-define',
                     dest='show_define', action='store_true',
                     help='show all macro define')
        p.add_option('-u', '--show-source',
                     dest='show_source', action='store_true',
                     help='show all source code file')
        p.add_option('-b', '--board',
                     dest='board_name', action='store', type='str', default=None,
                     help='specify board name')
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
        if opt.show_all:
            opt.show_component = True
            opt.show_libs = True
            opt.show_include = True
            opt.show_variables = True
            opt.show_define = True
            opt.show_flags = True
            opt.show_source = True
        elif not (opt.show_component or opt.show_libs or opt.show_include or opt.show_variables or opt.show_define or opt.show_flags or opt.show_source):
            opt.show_component = True
            opt.show_flags = True

        solution.show(show_component=opt.show_component, show_libs=opt.show_libs,
                      show_include=opt.show_include, show_veriable=opt.show_variables,
                      show_define=opt.show_define, show_flags=opt.show_flags)
        if opt.show_source:
            for c in solution.components:
                c.show()
                c.info(4)
