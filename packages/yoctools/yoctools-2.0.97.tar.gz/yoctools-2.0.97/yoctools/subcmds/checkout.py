# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *


class Checkout(Command):
    common = True
    helpSummary = "Checkout a branch for development"
    helpUsage = """
%prog [-b <branch>] [-f <logfile>] [<project>...]
"""
    helpDescription = """
Initialize yoc workspace in the current directory.
"""

    def _Options(self, p):
        p.add_option('-b', '--branch',
                     dest='branch', action='store', type='string',
                     help='checkout the branche for the component')
        p.add_option('-f', '--file',
                     dest='file', action='store', type='string',
                     help='checkout the commit from file')

    def Execute(self, opt, args):
        if not opt.branch and not opt.file:
            self.Usage()
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
        if opt.branch:
            np = Progress('Checkout %s' % opt.branch, len(components))
            for component in components:
                component.np = np
            for component in components:
                component.np.update(msg=component.name)
                git = GitRepo(component.path, component.repo_url)
                git.CheckoutBranch(opt.branch)
            np.end()
        elif opt.file:
            self.checkout_from_file(opt.file, components)

    def checkout_from_file(self, file_path, components):
        try:
            got = False
            with codecs.open(file_path, 'r', 'UTF-8') as f:
                contents = f.readlines()
                for i in range(len(contents) - 1):
                    c = contents[i]
                    idx = c.find('* ')
                    idx2 = c.find(':')
                    if idx > 0 and idx2 > 0:
                        name = c[idx + 2:idx2]
                        component = components.get(name)
                        if component:
                            c = contents[i + 1]  # commit id
                            idx = c.find('commit ')
                            if idx > 0:
                                start = idx + len('commit ')
                                end = start + 8
                                commitid = c[start:end]
                                put_string("Checkout %s: %s" % (commitid, name))
                                git = GitRepo(component.path, component.repo_url)
                                git.CheckoutBranch(commitid)
                                got = True
            if not got:
                put_string("There is nothing to checkout,maybe the file:`%s` format is not right." % file_path, level='warning')
        except Exception as ex:
            put_string("%s" % str(ex), level='error')