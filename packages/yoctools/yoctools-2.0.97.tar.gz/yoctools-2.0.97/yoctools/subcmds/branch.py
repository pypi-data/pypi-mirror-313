# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *


class Branch(Command):
    common = True
    helpSummary = "View current component branches"
    helpUsage = """
%prog [<compnent> ...]
"""
    helpDescription = """
View current component branches
"""
    def _Options(self, p):
        p.add_option('-a', '--all',
                     dest='show_all', action='store_true',
                     help='show the all branches for the component')
        p.add_option('-d', '--delete',
                     dest='delete', action='store', type='string',
                     help='delete the local branch for the component')
        p.add_option('-r', '--remote',
                     dest='remote', action='store_true',
                     help='delete the remote branch for the component')
        p.add_option('-f', '--format',
                     dest='format', action='store_true',
                     help='show the current actived branch infomation')
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
            branches = git.GetRemoteBranches('origin')
            if opt.remote:
                if opt.delete not in branches:
                    put_string("Can't find branch:%s in remote." % opt.delete, level='warning')
                    return
                ret = git.delete_branch(opt.delete, True)
                if ret:
                    put_string("Delete local and remote branch:%s for %s failed.(%s)" % (opt.delete, component.name, ret), level='warning')
                else:
                    put_string("Delete local and remote branch:%s for %s success." % (opt.delete, component.name))
            elif opt.delete:
                if git.delete_branch(opt.delete):
                    put_string("Delete local branch:%s for %s failed." % (opt.delete, component.name), level='warning')
                else:
                    put_string("Delete local branch:%s for %s success." % (opt.delete, component.name))
            else:
                ab, _ = git.safe_active_branch()
                if opt.format:
                    put_string("%-24s %-8s %s" % (component.name, ab, git.repo.head.commit.hexsha), color='green')
                else:
                    put_string(component.name + ':')
                    put_string('  * %s' % ab, color='green')
                if opt.show_all:
                    for b in branches:
                        put_string('  %s' % b, color='red')
