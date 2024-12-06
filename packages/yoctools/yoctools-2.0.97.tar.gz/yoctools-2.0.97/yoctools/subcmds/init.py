# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

import os
from yoctools import *

manifeset_aone_url='git@gitlab.alibaba-inc.com:yocopen/manifest.git'
manifeset_gerrit_url='ssh://gerrit.damo.xrvm.cn:29518/yocopen/manifest.git'
gerrit_commit_msg_url = 'https://gerrit.damo.xrvm.cn/tools/hooks/commit-msg'

class Init(Command):
    common = True
    helpSummary = "Initialize yoc workspace in the current directory"
    helpUsage = """
%prog [repo] [option] <branch>
"""
    helpDescription = """
Initialize yoc workspace in the current directory.
"""
    def _Options(self, p):
        p.add_option('-a', '--aone',
                     dest='aone', action='store_true',
                     help='init manifeset repo from aone')
        p.add_option('-g', '--gerrit',
                     dest='gerrit', action='store_true',
                     help='init manifeset repo from gerrit')
        p.add_option('-b', '--branch',
                     dest='branch', action='store', type='string',
                     help='the manifest repo branch')

    def Execute(self, opt, args):
        conf = Configure()
        yoc_file_path = os.path.join(conf.yoc_path, '.yoc')
        if conf.init:
            put_string("Workspace is initialized already.", level='warning')
            put_string("The workspace is `%s`" % conf.yoc_path)
            instr = raw_input("Do you want to init again? Y(es) or N(o)?\n")
            if instr.upper() == 'Y' or instr.upper() == 'YES':
                repo_dir = os.path.join(conf.yoc_path, '.repo')
                if os.path.exists(repo_dir):
                    shutil.rmtree(repo_dir)
                if os.path.isfile(yoc_file_path):
                    os.remove(yoc_file_path)
            else:
                return
        try:
            urlretrieve('https://yoctools.oss-cn-beijing.aliyuncs.com/yoc_new', yoc_file_path)
        except:
            pass
        if os.path.isfile(yoc_file_path):
            conf.load(yoc_file_path)
        if opt.branch:
            conf.branch = opt.branch
        if opt.aone:
            conf.repo = manifeset_aone_url
        if opt.gerrit:
            conf.repo = manifeset_gerrit_url
            conf.commit_msg_url = gerrit_commit_msg_url
        if len(args) > 0:
            conf.repo = args[0] # repourl
        conf.save()
