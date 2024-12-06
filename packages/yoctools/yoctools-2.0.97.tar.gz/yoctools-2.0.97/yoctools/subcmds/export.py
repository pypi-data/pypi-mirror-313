# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *
import os
import shutil

class Export(Command):
    common = True
    helpSummary = "Export component to dest directory"
    helpUsage = """
%prog <component> [<component> <component> ...] <dest path>
"""
    helpDescription = """
Export component to dest directory
"""

    def Execute(self, opt, args):
        if len(args) < 2:
            self.Usage()

        yoc = YoC()
        componentList = args[:-1]
        destPath = args[-1]
 
        if yoc.conf.yoc_path == os.path.abspath(destPath):
            put_string("Can't export to the same path.", level='error')
            return

        for c in componentList:
            if not yoc.components.get(c):
                put_string("There is no component:%s found in workspace." % c, level='warning')
        count = 0
        for component in yoc.components:
            if component.name in componentList:
                component.load_package()
                depend = yoc.check_depend(component)
                for d in depend:
                    self.component_export(d, destPath)
                    count += 1
                self.component_export(component, destPath)
                count += 1
        if count:
            yoc.conf.save(os.path.join(destPath, '.yoc'))


    def component_export(self, component, path):
        if component.type in ['common', 'chip', 'sdk']:
            p = 'components'
        elif component.type == 'board':
            p = 'boards'
        elif component.type == 'solution':
            p = 'solutions'
        if p:
            dest = os.path.join(path, p, component.name)
            put_string("Export `%s` to %s." % (component.name, dest))
            try:
                if os.path.exists(dest):
                    shutil.rmtree(dest)
                shutil.copytree(component.path, dest)
            except Exception as ex:
                put_string(str(ex), level='error')
                pass
