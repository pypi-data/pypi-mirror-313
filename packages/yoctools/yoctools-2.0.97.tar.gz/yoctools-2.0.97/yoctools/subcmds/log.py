# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

import threadpool
import time
import os
from yoctools import *


class Log(Command):
    common = True
    helpSummary = "Show the working tree log"
    helpUsage = """
%prog [<component>...]
"""
    helpDescription = """
Show the working tree log
"""

    def _Options(self, p):
        self.jobs = 1
        # p.add_option('-j', '--jobs',
        #              dest='jobs', action='store', type='int',
        #              help="projects to fetch simultaneously (default %d)" % self.jobs)

    def Execute(self, opt, args):
        yoc = YoC()

        # if opt.jobs:
        #     jobs = opt.jobs
        # else:
        #     jobs = 4
        jobs = 1

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

        # np = Progress('Showing projects', len(components), print_newline=True, force_show=True)
        task_pool = threadpool.ThreadPool(jobs)
        tasks = []
        for component in components:
            # component.np = np
            tasks.append(component)

        def thread_execture(component):
            # component.np.update(msg=component.name)
            git = GitRepo(component.path, component.repo_url)
            git.gitlog()

        requests = threadpool.makeRequests(thread_execture, tasks)
        for req in requests:
            task_pool.putRequest(req)
        task_pool.wait()
        task_pool.dismissWorkers(jobs, do_join=True)

        # np.end()
