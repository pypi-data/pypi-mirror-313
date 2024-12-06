# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *
import shutil


class Gitrun(Command):
    common = True
    helpSummary = "Run git cmd with a external script"
    helpUsage = """
%prog -s <script> [<project>...]
"""
    helpDescription = """
Run git cmd with a external script in component path.
"""

    def _Options(self, p):
        p.add_option('-s', '--script',
                     dest='script', action='store', type='string',
                     help='the git cmd script file')

    def Execute(self, opt, args):
        if not opt.script:
            self.Usage()
            return
        if not os.path.isfile(opt.script):
            put_string("%s is not a file.", opt.script, level='error')
            return
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
        pwd = os.getcwd()
        git_script = os.path.abspath(opt.script)
        count = 0
        for component in components:
            count = count + 1
            put_string("[%d/%d] I am in %s ..." % (count, len(components), component.name))
            tmp_script = os.path.join(component.path, "tmpgit_" + component.name + '.sh')
            # print(os.getcwd(), tmp_script)
            shutil.copy2(git_script, tmp_script)
            os.chdir(component.path)
            if os.system('sh %s' % tmp_script) != 0:
                put_string("Excute git script in %s failed." % component.path, level='warning')
                continue
            os.remove(tmp_script)
        os.chdir(pwd)
        # print(os.getcwd())
