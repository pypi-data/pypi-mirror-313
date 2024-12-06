# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

import threadpool
from yoctools import *

global commit_msg_txt

class Install(Command):
    common = True
    helpSummary = "Install component into project environment"
    helpUsage = """
%prog [option] [<component>...]
"""
    helpDescription = """
Install component into project environment
"""

    def _Options(self, p):
        self.jobs = 1
        p.add_option('-j', '--jobs',
                     dest='jobs', action='store', type='int',
                     help="projects to fetch simultaneously (default %d)" % self.jobs)
        p.add_option('-f', '--force',
                     dest='force', action='store_true',
                     help='install component force if exist already')
        p.add_option('-b', '--branch',
                     dest='branch', action='store', type='string',
                     help='the branch for component to download')
        p.add_option('-s', '--single',
                     dest='single', action='store_true',
                     help='just install one component, exclude its\' dependent components')

    def Execute(self, opt, args):
        if opt.jobs:
            jobs = opt.jobs
        else:
            jobs = 4
        put_string("Start to install components...")
        yoc = YoC()
        components = ComponentGroup()
        if len(args) > 0:
            for name in args:
                update = False
                if name == args[0]:
                    update = True
                cmpt = yoc.check_cmpt_download(name, update=True, force=opt.force)
                if cmpt:
                    components.add(cmpt)
        else:
            yoc.update()
            components = yoc.occ_components

        def __post_function(comp_path):
            global commit_msg_txt
            try:
                if yoc.conf.commit_msg_url and os.path.exists(comp_path):
                    cmsg_file = os.path.join(comp_path, ".git/hooks/commit-msg")
                    if not os.path.exists(cmsg_file):
                        with codecs.open(cmsg_file, 'w', 'UTF-8') as f:
                            if sys.version_info.major == 2:
                                if type(commit_msg_txt) == str:
                                    commit_msg_txt = commit_msg_txt.decode('UTF-8')
                            f.write(commit_msg_txt)
                    if os.path.isfile(cmsg_file) and os.path.getsize(cmsg_file):
                        os.chmod(cmsg_file, stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            except Exception as e:
                put_string(str(e), level='warning')

        exe_dld_cmpt_list = ComponentGroup()
        if len(components) > 0:
            dled_cmpts = []
            dep_list = {}
            vercheck_list = {}
            while len(components) > 0:
                cmpts = components
                self.download(jobs, cmpts, opt.branch, postfunc=__post_function)
                if opt.single:
                    exe_dld_cmpt_list = components
                    break
                for c in cmpts:
                    if c.name not in dled_cmpts:
                        dled_cmpts.append(c.name)
                components = ComponentGroup()
                for c in cmpts:
                    exe_dld_cmpt_list.add(c)
                    ret = c.load_package()
                    if ret:
                        yoc.update_version(c.depends) # 更新需要下载的组件的版本号，从父组件的depends字段下的版本号来
                        cmpt_list = self.get_need_download_cmpts(args, dled_cmpts, c, dep_list, vercheck_list)
                        for component in yoc.occ_components:
                            if component.name in cmpt_list:
                                components.add(component)
            # check different version
            self.show_vercheck_list(vercheck_list)
            # check file
            for c in exe_dld_cmpt_list:
                if not c.check_file_integrity():
                    put_string("Component:%s maybe not fetch integrallty(miss `README.md` or `package.yaml`), Please check the branch is right." % c.name, level='warning')
            put_string('Download components finish.')
        else:
            put_string("No component need to install.")

    def get_need_download_cmpts(self, origin_list, downloaded_list, component, dep_list={}, vercheck_list={}):
        cmpt_list = []
        for name in component.depends:
            if type(name) == dict:
                version = list(name.values())[0]
                name = list(name.keys())[0]
                if (name not in origin_list) and (name not in downloaded_list):
                    cmpt_list.append(name)
                ##################################check_depend_version
                for k, v in dep_list.items():
                    son = k.split(':')[0]
                    ver = k.split(':')[1]
                    if son == name and ver != version:
                        vercheck_list["%s:%s" % (name, version)] = {"father":component.name}
                        vercheck_list[k] = v
                key = "%s:%s" % (name, version)
                if key not in dep_list:
                    dep_list[key] = {"father":component.name}
                ##################################
        return cmpt_list

    def show_vercheck_list(self, vercheck_list):
        for k in sorted(vercheck_list):
            son = k.split(':')[0]
            ver = k.split(':')[1]
            father = vercheck_list[k]["father"]
            put_string("version_check: %s: %s in %s's depends." % (son, ver, father), level='warning')

    def download(self, jobs, components, branch, postfunc):
        task_pool = threadpool.ThreadPool(jobs)
        tasks = []
        for component in components:
            tasks.append(component)

        def thread_execture(component):
            component.download(branch, postfunc)

        requests = threadpool.makeRequests(thread_execture, tasks)
        for req in requests:
            task_pool.putRequest(req)
        task_pool.wait()
        task_pool.dismissWorkers(jobs, do_join=True)

commit_msg_txt = '''
#!/bin/sh
# From Gerrit Code Review 3.6.1
#
# Part of Gerrit Code Review (https://www.gerritcodereview.com/)
#
# Copyright (C) 2009 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -u

# avoid [[ which is not POSIX sh.
if test "$#" != 1 ; then
  echo "$0 requires an argument."
  exit 1
fi

if test ! -f "$1" ; then
  echo "file does not exist: $1"
  exit 1
fi

# Do not create a change id if requested
if test "false" = "$(git config --bool --get gerrit.createChangeId)" ; then
  exit 0
fi

if git rev-parse --verify HEAD >/dev/null 2>&1; then
  refhash="$(git rev-parse HEAD)"
else
  refhash="$(git hash-object -t tree /dev/null)"
fi

random=$({ git var GIT_COMMITTER_IDENT ; echo "$refhash" ; cat "$1"; } | git hash-object --stdin)
dest="$1.tmp.${random}"

trap 'rm -f "${dest}"' EXIT

if ! git stripspace --strip-comments < "$1" > "${dest}" ; then
   echo "cannot strip comments from $1"
   exit 1
fi

if test ! -s "${dest}" ; then
  echo "file is empty: $1"
  exit 1
fi

reviewurl="$(git config --get gerrit.reviewUrl)"
if test -n "${reviewurl}" ; then
  if ! git interpret-trailers --parse < "$1" | grep -q '^Link:.*/id/I[0-9a-f]\{40\}$' ; then
    if ! git interpret-trailers \
          --trailer "Link: ${reviewurl%/}/id/I${random}" < "$1" > "${dest}" ; then
      echo "cannot insert link footer in $1"
      exit 1
    fi
  fi
else
  # Avoid the --in-place option which only appeared in Git 2.8
  # Avoid the --if-exists option which only appeared in Git 2.15
  if ! git -c trailer.ifexists=doNothing interpret-trailers \
        --trailer "Change-Id: I${random}" < "$1" > "${dest}" ; then
    echo "cannot insert change-id line in $1"
    exit 1
  fi
fi

if ! mv "${dest}" "$1" ; then
  echo "cannot mv ${dest} to $1"
  exit 1
fi
'''