# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *


class List(Command):
    common = True
    helpSummary = "List component"
    helpUsage = """
%prog [option] [<component> ...]
"""
    helpDescription = """
List all projects; pass '.' to list the project for the cwd.
"""

    def _Options(self, p):
        p.add_option('-r', '--remote',
                     dest='show_remote', action='store_true',
                     help='show OCC all compoent')

        p.add_option('-b', '--board',
                     dest='board', action='store_true',
                     help='list all board component')

        p.add_option('-s', '--solution',
                     dest='solution', action='store_true',
                     help='list all soution component')

        p.add_option('-c', '--chip',
                     dest='chip', action='store_true',
                     help='list all chip component')

        p.add_option('-m', '--common',
                     dest='common', action='store_true',
                     help='list all common component')

        p.add_option('-k', '--sdk',
                     dest='sdk', action='store_true',
                     help='list all sdk component')

        p.add_option('-d', '--depend',
                     dest='depend', action='store_true',
                     help='list component dependencies')

    def Execute(self, opt, args):
        yoc = YoC()

        count = len(args)

        if opt.show_remote:
            yoc.update(True)
            components = yoc.occ_components
        else:
            components = yoc.components
            for c in components:
                if count == 0 or c.name in args:
                    c.load_package()
        
        if len(components) == 0:
            put_string("There is no component found!", level='warning')
            exit(-1)

        nonexistent_cnt = 0
        name_list = yoc.get_name_list(components)
        for name in args:
            if name not in name_list:
                put_string("Can't found component `%s`!" % name, level='warning')
                nonexistent_cnt+=1

        show = opt.board or opt.chip or opt.common or opt.solution or opt.sdk
        show_cnt = 0
        for c in components:
            if count == 0 or c.name in args:
                if show:
                    if (opt.board and c.type == 'board') or (opt.chip and c.type == 'chip') \
                        or (opt.common and c.type == 'common') or (opt.solution and c.type == 'solution') \
                        or (opt.sdk and c.type == 'sdk'):
                        self.show_depend(yoc, c, opt.depend)
                        show_cnt+=1
                else:
                    self.show_depend(yoc, c, opt.depend)
                    show_cnt +=1
        if show_cnt == 0 and nonexistent_cnt == 0:
            put_string('No matched component found!', level='warning')

    def show_depend(self, yoc, component, show_depend=False):
        component.load_package()
        component.show()
        if show_depend:
            depend = yoc.check_depend(component)
            if len(depend) > 0:
                put_string("    depends:")
                depend.show(8)
            depend_on = yoc.check_depend_on(component)
            if len(depend_on) > 0:
                put_string("    be depended(被依赖):")
                depend_on.show(8)
