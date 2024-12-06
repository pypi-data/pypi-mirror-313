# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
import os
import shutil
import pickle
import json
import codecs

from .tools import *
from .component import *
from .manifest import *
from .occ import *
from .log import logger
from .solution import *
from .repo import *


class Configure:
    def __init__(self):
        self.lastUpdateTime = 0
        self.gitlab_token = ''
        self.github_token = ''
        self.gitee_token = ''
        self.group = 'yocop'
        self.username = ''
        self.password = ''
        self.occ_host = 'www.xrvm.cn'
        self.repo = 'https://gitee.com/yocop/manifest.git'
        self.branch = 'master'       # manifest.git的branch
        self.init = False
        self.commit_msg_url = ''

        self.yoc_path = os.getcwd()
        if not self.yoc_path:
            self.yoc_path = '/'
        tmp_path = self.yoc_path
        while tmp_path != '/':
            f = os.path.join(tmp_path, '.yoc')
            if os.path.exists(f):
                self.yoc_path = tmp_path
                conf = yaml_load(f)
                if conf:
                    self.init = True
                    for k, v in conf.items():
                        if v:
                            self.__dict__[k] = v
                break
            tmp_path = os.path.dirname(tmp_path)

        if self.repo:
            if self.repo.endswith('.git'):
                if self.repo.startswith('http'):    # like 'https://gitee.com/yocop/manifest.git'
                    self.group = self.repo.split('/')[-2]
                elif self.repo.startswith('git@'):  # like 'git@gitlab.alibaba-inc.com:yocopen/manifest.git'
                    self.group = self.repo.split(':')[-1].split('/')[-2]
                elif self.repo.startswith('ssh://gerrit.damo'):  # like 'ssh://gerrit.damo.xrvm.cn:29518/yocopen/manifest.git'
                    self.group = self.repo.split('/')[-2]
                else:
                    put_string('The repo is wrong!', level='warning')
            else:
                if self.repo.startswith('http'):    # like 'https://gitee.com/yocop'
                    self.group = self.repo.split('/')[-1]
                elif self.repo.startswith('git@'):  # like 'git@gitlab.alibaba-inc.com:yocopen'
                    self.group = self.repo.split(':')[-1]
                elif self.repo.startswith('ssh://gerrit.damo'):  # like 'ssh://gerrit.damo.xrvm.cn:29518/yocopen'
                    self.group = self.repo.split('/')[-1]
                else:
                    put_string('The repo is wrong!', level='warning')
    def load(self, yoc_file):
        if os.path.isfile(yoc_file):
            conf = yaml_load(yoc_file)
            if conf:
                for k, v in conf.items():
                    self.__dict__[k] = v

    def save(self, yoc_file=None):
        if not yoc_file:
            yoc_file = os.path.join(self.yoc_path, '.yoc')
        with codecs.open(yoc_file, 'w', 'UTF-8') as f:
            for k, v in self.__dict__.items():
                if k not in ['yoc_path', 'init', 'group', 'yoc_version'] and v:
                    f.write("{}: {}\n".format(k, v))
        self.init = True

    def search_pacakge_yaml(self, subpath=[], sub_prefix=[]):

        def traversalDir_FirstDir(path):
            list = []
            if (os.path.exists(path)):
                files = os.listdir(path)
                for file in files:
                    m = os.path.join(path,file)
                    if (os.path.isdir(m)):
                        h = os.path.split(m)
                        list.append(h[1])
                return list

        paths = []
        if subpath or sub_prefix:
            if subpath:
                for sub in subpath:
                    p = os.path.join(self.yoc_path, sub)
                    if os.path.exists(p):
                        paths.append(p)
            if sub_prefix:
                first_dir = traversalDir_FirstDir(self.yoc_path)
                for d in first_dir:
                    for sub in sub_prefix:
                        if d.startswith(sub):
                            p = os.path.join(self.yoc_path, d)
                            paths.append(p)
        else:
            paths.append(self.yoc_path)

        package_list = []

        while paths:
            path = paths[0]
            filename = os.path.join(path, 'package.yaml')
            if os.path.isfile(filename):
                package_list.append(filename)
            else:
                files = os.listdir(path)
                for file in files:
                    p = os.path.join(path, file)
                    if os.path.isdir(p):
                        paths.append(p)
            del paths[0]
        return package_list


class YoC:
    def __init__(self):
        self.occ = None
        self.occ_components = None
        self.conf = Configure()
        self.yoc_path = self.conf.yoc_path

        try:
            compenent_db = os.path.join(self.yoc_path, '.components.db')
            with open(compenent_db, "rb") as f:
                self.occ_components = pickle.load(f)
                if len(self.occ_components) == 0:
                    self.occ_components = None
        except:
            self.occ_components = None

        if not self.occ_components:
            self.conf.lastUpdateTime = 0

        # scanning yoc all components
        self.components = ComponentGroup()
        package_yamls = self.conf.search_pacakge_yaml(
            ['boards', 'components', 'examples'], ['solutions'])

        filename = os.path.join(os.getcwd(), 'package.yaml')
        if os.path.isfile(filename):
            pack = Package(filename)
            if pack.type == 'solution':
                if filename not in package_yamls:
                    package_yamls.append(filename)

        for filename in package_yamls:
            pack = Component(self.conf, filename)

            if not self.components.add(pack):
                pre_component = self.components.get(pack.name)
                put_string('Component `%s` is multiple, first defined in :%s, redifned here: %s, please check!)' %
                             (pack.name, pre_component.path, pack.path), level='error')
                exit(0)

    def clone_manifest(self, is_all=False):
        manifest_path = os.path.join(self.yoc_path, ".repo")
        if not os.path.exists(manifest_path):
            os.mkdir(manifest_path)
        repo_url = self.conf.repo
        git = GitRepo(manifest_path, repo_url)
        if is_all:
            git.pull('master', None)
        else:
            git.pull(self.conf.branch, None)

    def sync_manifest(self):
        manifest_path = os.path.join(self.yoc_path, ".repo")
        if os.path.exists(manifest_path):
            repo_url = self.conf.repo
            git = GitRepo(manifest_path, repo_url)
            git.pull(self.conf.branch, None)

    def manifest_yaml_parse(self, filename=None):
        if not filename:
            filename = os.path.join(self.yoc_path, ".repo/default.yaml")
        if os.path.isfile(filename):
            mani = Manifest(filename)
            return mani
        else:
            put_string("Can't find %s" % filename, level='warning')
            put_string("Maybe there is no branch(%s) in %s" % (self.conf.branch, self.conf.repo))

    def get_name_list(self, group):
        name_list = []
        for c in group:
            name_list.append(c.name)
        return name_list

    def check_depend(self, component):
        def _check_depend(component):
            component.load_package()

            for name in component.depends:
                if type(name) == dict:
                    name = list(name.keys())[0]
                c = self.components.get(name)
                if c:
                    if c not in depend_cmpts:
                        depend_cmpts.append(c)
                    if component not in c.depends_on:
                        c.depends_on.append(component)
                    _check_depend(c)

        depend_cmpts = ComponentGroup()

        _check_depend(component)
        return depend_cmpts

    def check_depend_on(self, component):
        depends_on = ComponentGroup()
        for c in self.components:
            c.load_package()
            for d in c.depends:
                if component.name in d:
                    depends_on.append(c)
        return depends_on

    def getSolution(self, board_name=None, sdk_name=None, not_filter=False, file_non_existent_no_err=False):
        if board_name and sdk_name:
            put_string("Can't specify BOARD and SDK name at one time.", level='error')
            exit(-1)
        board_name_in_sdkchip = []
        for component in self.components:
            if component.path == os.getcwd():
                component.load_package()
                if sdk_name or len(component.sdk_chip) > 0:
                    if not sdk_name:
                        for name in component.depends:
                            if type(name) == dict:
                                name = list(name.keys())[0]
                                c = self.components.get(name)
                                if c and c.load_package() and c.type == 'sdk':
                                    sdk_name = name
                                    break
                        if not sdk_name:
                            for i in range(len(component.sdk_chip)):
                                sdk_name = list((component.sdk_chip[i]).keys())[0]
                                sdk_comp = self.components.get(sdk_name)
                                if sdk_comp:
                                    break
                    sdk_comp = self.components.get(sdk_name)
                    if not sdk_comp:
                        put_string("Sdk chip component `%s` not found in current workspace, please install it: yoc install %s " %(sdk_name, sdk_name), level='error')
                        exit(-1)
                    else:
                        sdk_comp.load_package()
                        for name in sdk_comp.depends:
                            if type(name) == dict:
                                name = list(name.keys())[0]
                            c = self.components.get(name)
                            if c:
                                c.load_package()
                                if c.type == 'board':
                                    board_name_in_sdkchip.append(c.name)

                if len(board_name_in_sdkchip) > 1:
                    put_string("Sdk chip component `%s` includes multi boards, please check." % sdk_name, level='error')
                    exit(-1)
                elif len(board_name_in_sdkchip) == 1:
                    component.hw_info.board_name = board_name_in_sdkchip[0]
                if board_name:
                    if self.components.get(board_name):
                        component.hw_info.board_name = board_name
                    else:
                        put_string("Board component `%s` not found in current workspace, please install it: yoc install %s " %(board_name, board_name), level='error')
                        exit(-1)
                # append current sdk chip components to depends filed.
                for d in component.sdk_chip:
                    if d not in component.depends:
                        if sdk_name == list(d.keys())[0]:
                            component.depends.append(d)

                # 根据指定的board_name过滤其他的board组件
                exclude_names = []
                for name in component.depends:
                    if type(name) == dict:
                        name = list(name.keys())[0]
                    c = self.components.get(name)
                    if c:
                        c.load_package()
                        if c.type == 'board' and name != component.hw_info.board_name:
                            if name not in exclude_names:
                                exclude_names.append(name)
                        if sdk_name:
                            if c.type == 'sdk' and name != sdk_name:
                                if name not in exclude_names:
                                    exclude_names.append(name)
                if not_filter:
                    exclude_names = []
                    for d in component.sdk_chip:
                        if d not in component.depends:
                            component.depends.append(d)

                components, lost = self.components.get_depend(component, exclude_names)
                if lost:
                    exit(-1)
                components.add(component)
                solution = Solution(components, file_non_existent_no_err)

                return solution

    def check_cmpt_download(self, name, update=True, force=False):
        if self.components.get(name) and not force:
            put_string("Component `%s` have installed already! Skip to install it! You can add '-f' option to force installation." % name, level='warning')
        else:
            if update:
                self.update()
            if self.occ_components:
                component = self.occ_components.get(name)
                if component:
                    return component
                else:
                    put_string("Can't find component %s." % name, level='warning')
            else:
                put_string("There is no component found from server!", level='warning')
        return None

    def download_component(self, name, update=True, force=False):
        if self.components.get(name) and not force:
            put_string("Component `%s` have installed already! Please add -f option to install force!" % name, level='warning')
            return None
        if self.components.get(name) == None or force:
            if update:
                # self.occ_update()
                self.gitee_update()

            component = self.occ_components.get(name)
            if component:
                depends, _ = self.occ_components.get_depend(component)
                depends.add(component)

                return depends
            else:
                put_string("There is no component `%s` found from repo!" % name, level='warning')

    def remove_component(self, name):
        component = self.components.get(name)
        if component:
            if not component.depends_on:                     # 如果没有组件依赖它
                for n in component.depends:
                    if type(n) == dict:
                        n = list(n.keys())[0]
                    p = self.components.get(n)
                    if p:
                        if name in p.depends_on:
                            del p.depends_on[name]
                        self.remove_component(n)

                shutil.rmtree(component.path)
                self.components.remove(component)
                return True
            else:
                logger.info("remove fail, %s depends on:" % component.name)
                for dep in component.depends_on:
                    logger.info('  ' + dep.name)
                return False

    def occ_login(self):
        if self.occ == None:
            self.occ = OCC(self.conf)
        if not self.occ.login():
            put_string("Login OCC failed. Please check your username and password.", level='error')
            return False
        return True

    def upload(self, name):
        component = self.components.get(name)
        if component:
            component.load_package()
            version = component.version
            if version:
                if not os.path.isdir(os.path.join(component.path, '.git')):
                    if self.occ == None:
                        self.occ = OCC(self.conf)
                    self.occ.login()
                    zip_file = component.zip(self.yoc_path)
                    if self.occ.upload(version, component.type, zip_file) == 0:
                        put_string("Component %s(%s) upload success!" % (component.name, version))
                    else:
                        put_string("Component %s(%s) upload failed!" % (component.name, version), level='warning')
                else:
                    put_string("It is a git repo,abort to upload.", level='warning')
            else:
                put_string("Component %s version is empty!" % (component.name), level='warning')

    def uploadall(self):
        if self.occ == None:
            self.occ = OCC(self.conf)
        self.occ.login()
        for component in self.components:
            component.load_package()
            version = component.version
            if version:
                zip_file = component.zip(self.yoc_path)
                if self.occ.upload(version, component.type, zip_file) == 0:
                    put_string("Component %s(%s) upload success!" % (component.name, version))
                else:
                    put_string("Component %s(%s) upload failed!" % (component.name, version), level='warning')
            else:
                put_string("Component %s version is empty!" % (component.name), level='warning')

    def update(self, is_all=False):
        def get_repo_url(remotes, cmp_ele):
            if cmp_ele.remote.startswith('https://') \
                or cmp_ele.remote.startswith('http://') \
                or cmp_ele.remote.startswith('git@') \
                or cmp_ele.remote.startswith('ssh://'):
                return cmp_ele.remote
            else:
                for r in remotes:
                    if cmp_ele.remote == r.name:
                        repo_url = os.path.join(r.remote, '%s.git' % cmp_ele.name)
                        return repo_url
        def get_cmpt_path(name, type):
            if type == 'board':
                path = os.path.join('boards', name)
            elif type == 'solution':
                path = os.path.join('solutions', name)
            else:
                path = os.path.join('components', name)
            return os.path.join(self.conf.yoc_path, path)

        self.clone_manifest(is_all)
        self.default_mani = self.manifest_yaml_parse()
        if self.default_mani:
            self.occ_components = ComponentGroup()
            for p in self.default_mani.cmpt_list:
                cmp = Component(self.conf)
                cmp.name = p.name
                cmp.type = p.type
                cmp.description = p.desc
                cmp.repo_url = get_repo_url(self.default_mani.remotes, p)
                cmp.path = get_cmpt_path(cmp.name, cmp.type)
                # print(cmp.name, cmp.type, cmp.repo_url, cmp.description, cmp.path)
                self.occ_components.add(cmp)
            with open(os.path.join(self.yoc_path, '.components.db'), "wb") as f:
                pickle.dump(self.occ_components, f)
                self.conf.save()

    def get_latest_version(self, component):
        for p in self.default_mani.cmpt_list:
            if component.name == p.name and len(p.history_ver):
                latest_ver = latest_ver_get(component.version, p.history_ver[len(p.history_ver) - 1])
                return latest_ver

    def update_version(self, depends=[]):
        for component in self.occ_components:
            for d in depends:
                if type(d) == dict:
                    name = list(d.keys())[0]
                    if component.name == name:
                        component.version = list(d.values())[0]
                        latest_ver = self.get_latest_version(component)
                        if latest_ver and component.version != latest_ver:
                            component.version = latest_ver
                            # print('latest_ver========%s,%s' % (latest_ver, component.name))
                        # print("update %s version:%s" % (component.name, component.version))
                        break
            
    def gitee_update(self):
        self.occ_components = ComponentGroup()
        if not self.conf.gitee_token:
            put_string("Can't fetch from git repo, please check your `.yoc` file.", level='error')
            return
        put_string("Updating from git...")
        repo = RepoGitee(self.conf.gitee_token, self.conf.group)
        for p in repo.projects():
            pack = Component(self.conf)
            if p:
                if type(p) == bytes:
                    p = bytes.decode(p)
                pack.loader_json(json.loads(p))
                pack.path = os.path.join(self.conf.yoc_path, pack.path)
                self.occ_components.add(pack)
        with open(os.path.join(self.yoc_path, '.components.db'), "wb") as f:
            pickle.dump(self.occ_components, f)
            self.conf.save()

    def occ_update(self):
        if self.occ == None:
            self.occ = OCC(self.conf)
        put_string("Updating from OCC...Please wait.")
        components, time = self.occ.yocComponentList('614193542956318720', self.conf.lastUpdateTime)
        put_string("Update from OCC over.")
        if components:
            self.occ_components = components
            self.conf.lastUpdateTime = time
            for component in self.occ_components:
                component.path = os.path.join(self.yoc_path, component.path)

            with open(os.path.join(self.yoc_path, '.components.db'), "wb") as f:
                pickle.dump(self.occ_components, f)
                self.conf.save()

    def list(self):
        for component in self.components:
            component.load_package()
            component.show()
