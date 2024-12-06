# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *


class Tag(Command):
    common = True
    helpSummary = "View current component tags"
    helpUsage = """
%prog [<compnent> ...]
"""
    helpDescription = """
View current component tags
"""
    def _Options(self, p):
        p.add_option('-l', '--latest',
                     dest='latest', action='store_true',
                     help='Fetch the latest tag.')

    def Execute(self, opt, args):
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

        for component in components:
            git = GitRepo(component.path, component.repo_url)
            tags = git.GetRemoteTags()
            if opt.latest:
                put_string(component.name + ':', color='orange')
                if len(tags) > 0:
                    last = "v0.0.0"
                    for tag in tags:
                        t = tag.name
                        if t.startswith('v') and not re.search("\.{2,10}", t[1:]) and re.search("^\d+(\.\d+){0,10}$", t[1]):
                            last = get_max_version(last, t)
                    put_string(" - %s" % last)
                else:
                    put_string(' - NULL')
            else:
                if len(tags) > 0:
                    put_string(component.name + ':')
                    for b in tags:
                        put_string('  %s' % b)