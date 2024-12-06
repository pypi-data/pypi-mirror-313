# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


import os
import sys
import shutil
import git
import time

from .log import *
from .tools import *


class simpleProgressBar(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        # text = "%3d%% (%d/%d)" % (cur_count/(max_count or 100.0), cur_count, max_count)
        sys.stdout.write(self._cur_line)
        sys.stdout.flush()
        if op_code & self.END:
            sys.stdout.write('\n')
        else:
            sys.stdout.write('\r')


class pullProgressBar(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        sys.stdout.write(self._cur_line)
        sys.stdout.flush()
        if op_code & self.END:
            sys.stdout.write('\n')
        else:
            sys.stdout.write('\r')


class GitRepo:
    def __init__(self, path, repo_url=None):
        self.repo_url = repo_url
        self.path = path
        git_path = os.path.join(path, '.git')

        if not os.path.exists(git_path):  # 如果未下载，则 git clone 下来
            self.repo = git.Repo.init(path)
        else:
            try:
                self.repo = git.Repo(path)
            except Exception as ex:
                self.repo = git.Repo.init(path)

        if repo_url:
            self.set_remote(repo_url)

    def set_remote(self, repo_url):
        try:
            origin = self.repo.remote()
            origin.set_url(repo_url)
        except Exception as ex:
            origin = self.repo.create_remote(name='origin', url=repo_url)
            try:
                origin.fetch()
            except Exception as ex:
                info = str(ex)
                if info.find("Please make sure you have the correct access rights") > 0:
                    put_string("%s" % origin.url, level='warning')
                    put_string("Please make sure you have the correct access rights and the repository exists", level='warning')

    def pull(self, version='', progress=pullProgressBar()):
        try:
            if not version:
                version = self.repo.active_branch

            origin = self.repo.remote()

            if version not in self.repo.heads:
                if version not in origin.refs:
                    origin.fetch(progress=progress)
                if version in origin.refs:
                    branch = self.repo.create_head(version, origin.refs[version])
                    branch.set_tracking_branch(origin.refs[version])
                    branch.checkout()
                elif origin.fetch("--tags") and version in self.repo.tags:
                    git = self.repo.git
                    git.checkout(version, b=version)         # create a new branch, name same as tag
                else:
                    # commit id
                    git = self.repo.git
                    git.checkout(version)
            else:
                if version in origin.refs:
                    origin.pull(version)
                    self.repo.heads[version].set_tracking_branch(origin.refs[version])
                else:
                    origin.pull()

        except Exception as ex:
            info = str(ex)
            if info.find('Please make sure you have the correct access rights') > 0:
                put_string("%s" % origin.url, level='warning')
                put_string("Please make sure you have the correct access rights and the repository exists.", level='warning')
            # put_string("\nPull %s occur error:(%s)" % (origin.url, str(ex)), level='warning')
            pass

    def fetch(self, remote="origin"):
        try:
            remote = self.repo.remote(remote)
        except ValueError:
            msg = "Remote {remote} does not exist on repo {repo}".format(
                remote=remote,
                repo=self.repo.repo.working_dir
            )
            logger.error(msg)
        try:
            remote.fetch(progress=pullProgressBar())
        except git.GitCommandError as ex:
            info = str(ex)
            if info.find('Please make sure you have the correct access rights') > 0:
                put_string("%s" % remote.url, level='warning')
                put_string("Please make sure you have the correct access rights and the repository exists.", level='warning')
                # print("Use: `yoc addkey`")


    def import_path(self, path, version):
        files = os.listdir(self.repo.working_dir)
        for f in files:
            if f != '.git':
                fn = os.path.join(self.repo.working_dir, f)
                if os.path.isdir(fn):
                    shutil.rmtree(fn)
                else:
                    os.remove(fn)

        for dirpath, _, filenames in os.walk(path):
            if dirpath.find(os.path.join(path, '.git')) < 0:
                for f in filenames:
                    p1 = os.path.join(dirpath, f)
                    p2 = os.path.relpath(p1, path)
                    p2 = os.path.join(self.repo.working_dir, p2)
                    try:
                        p = os.path.dirname(p2)
                        os.makedirs(p)
                    except:
                        pass

                    shutil.copy2(p1, p2)

        if self.repo.is_dirty(untracked_files=True):
            self.repo.git.add(self.repo.untracked_files)
            self.repo.git.commit('-m', 'init version', '-a')

            branch = self.repo.create_head(version)
            branch.checkout()

            self.repo.git.push(
                "--set-upstream", self.repo.remotes.origin, self.repo.head.ref)

    def GetRemoteBranches(self, remote='origin'):
        br_arr = []
        try:
            branches = self.repo.remote().refs
            for b in branches:
                if remote and remote in b.name:
                    br_arr.append(''.join(b.name.split('/')[1:]))
                else:
                    br_arr.append(b.name)
        except:
            pass
        return br_arr

    def GetRemoteTags(self, remote=''):
        origin = self.repo.remote()
        origin.fetch("--tags")
        return self.repo.tags

    def CheckoutBranch(self, version):
        if not version:
            return
        try:
            git = self.repo.git
            origin = self.repo.remote()
            if version not in self.repo.heads:
                if version not in origin.refs:
                    origin.fetch()
                if version in origin.refs:
                    branch = self.repo.create_head(version, origin.refs[version])
                    branch.set_tracking_branch(origin.refs[version])
                    branch.checkout()
                elif origin.fetch("--tags") and version in self.repo.tags:
                    git.checkout(version, b=version)         # create a new branch, name same as tag
                else:
                    try:
                        # put_string("Checkout commit id: %s" % version)
                        git.checkout(version, b=version)    # commit_id
                    except:
                        put_string("Can't find version/commit: %s, Checkout with HEAD." % version, level='warning')
                        git.checkout('HEAD')
            else:
                git.checkout(version)
        except Exception as ex:
            if str(ex).find("already exists.") > 0:
                put_string("Branch: %s already exists." % version, level='warning')
                return
            put_string(str(ex), level='error')

    def sync(self):
        name = os.path.basename(self.path)
        # if self.repo.is_dirty(untracked_files=False):
            # put_string("There are modified files in %s, please commit or stash first." % name, level='warning')
            # return
        try:
            git = self.repo.git
            ret = git.pull()
            if ret.find("Already up to date") < 0:
                put_string("%s:" % name, color='blue')
                put_string("%s" % ret, color='cyan')
        except Exception as e:
            errs = str(e)
            # print(errs)
            if errs.find("stderr: 'error: Your local changes to the following files would be overwritten by merge") > 0:
                if errs.rfind("Aborting'") > 0:
                    errs = errs[errs.find("stderr: '")+len("stderr: '"):errs.rfind("Aborting'")-1]
                else:
                    errs = errs[errs.find("stderr:"):]
                errs = "[%s] %s" % (name, errs)
                put_string(errs, level='warning')

    def status(self):
        def print_status(diff_ctx, color):
            for item in diff_ctx:
                m = item.a_path
                if item.new_file:
                    put_string("%8s%-32s" % ("", "new file:   " + m), color=color)
                elif item.deleted_file:
                    put_string("%8s%-32s" % ("", "deleted:    " + m), color=color)
                elif item.renamed:
                    put_string("%8s%-32s" % ("", "renamed:    " + m + " -> " + item.b_path), color=color)
                else:
                    put_string("%8s%-32s" % ("", "modified:   " + m), color=color)

        name = os.path.basename(self.path)
        untracked_files = self.repo.untracked_files # Untracked files, red
        diff_none_list = self.repo.index.diff(None) # Changes not staged for commit, red
        diff_head_list = self.repo.index.diff("HEAD", R=True) # Changes to be committed, green
        # print(diff_head_list)
        # print(diff_none_list)
        # print("untracked_files: ", untracked_files)
        if len(diff_none_list) > 0 or len(diff_head_list) > 0 or len(untracked_files) > 0:
            ab, is_detached = self.safe_active_branch()
            if is_detached:
                put_string("(HEAD detached at %s)" % ab)
            else:
                put_string("%s: on branch %s" % (name, ab))
        if len(diff_head_list) > 0:
            put_string("    Changes to be committed:")
            print_status(diff_head_list, 'green')
        if len(diff_none_list) > 0:
            put_string("    Changes not staged for commit:")
            print_status(diff_none_list, 'red')
        if len(untracked_files) > 0:
            put_string("    Untracked files:")
            for uf in untracked_files:
                put_string("%8s%-32s" % ("", uf), color='red')
        # git = self.repo.git
        # statusinfo = git.status()
        # if statusinfo.find("Changes not staged for commit:") > 0 or statusinfo.find("Untracked files:") > 0:
        #     put_string("%s:" % name)
        #     put_string("%s" % statusinfo, level='info')

    def gitlog(self):
        name = os.path.basename(self.path)
        put_string("* %s:" % name, color='magenta')
        headcommit = self.repo.head.commit
        put_string("    commit %s" % headcommit.hexsha, color='orange')
        put_string("    Author: %s <%s>" % (headcommit.author.name, headcommit.author.email))
        put_string("    Date:   %s" % time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(headcommit.authored_date)))
        # put_string(headcommit.author_tz_offset)
        # put_string(headcommit.committer.name)
        # put_string(headcommit.committed_date)
        put_string("")
        put_string("        %s" % headcommit.message)
    
    def gitlog_between_tags(self, tagA, tagB):
        # git log --pretty=oneline v7.6.1...v7.6.2
        def __getlog(git, tagA, tagB):
            try:
                if not tagA:
                    msg = git.log(tagB)
                else:
                    msg = git.log('--pretty=oneline', "%s...%s" % (tagA, tagB))
                return msg
            except Exception as e:
                put_string(str(e), level='error')
                if (str(e).find("unknown revision or path not in the working tree")) > 0:
                    return -2
        git = self.repo.git
        msg = __getlog(git, tagA, tagB)
        if msg == -2 and tagA:
            msg = __getlog(git, None, tagB)
            if msg == -2:
                msg = None
        return msg

    def commit(self, message=''):
        name = os.path.basename(self.path)
        if self.repo.is_dirty(untracked_files=True):
            try:
                index = self.repo.index
                changed = [ item.a_path for item in self.repo.index.diff(None) ]
                untracked_files = self.repo.untracked_files
                files = []
                for a in changed:
                    files.append(a)
                for a in untracked_files:
                    files.append(a)
                index.add(files)
                index.commit(message)
                remote = self.repo.remote()
                remote.push()
                put_string("Commit [%-24s] ok." % name)
            except Exception as ex:
                put_string("Commit [%-24s] failed(%s)." % (name, str(ex)), level='warning')
                return False
        return True

    def delete_branch(self, branch, is_remote=False):
        git = self.repo.git
        try:
            git.branch('-D', branch)
        except Exception as ex:
            # put_string("Delete branch:%s error(%s)." % (branch, str(ex)), level='warning')
            if not is_remote:
                return str(ex)
        if is_remote:
            try:
                git.push('origin', ':'+branch)
            except Exception as ex:
                return str(ex)
        return None

    def safe_active_branch(self):
        if self.repo.head.is_detached:
            return self.repo.head.commit.hexsha[:8], True
        else:
            return str(self.repo.active_branch), False

    def upload_to_gitee(self, component, new_tag):
        def _push_tag(git, new_tag):
            git.tag(new_tag)
            git.push('origin', "%s:refs/tags/%s" % (new_tag, new_tag))

        try:
            tmp1 = os.path.join('/tmp/yoc/aone', component.name)
            if os.path.exists(tmp1):
                shutil.rmtree(tmp1)
            os.makedirs(tmp1, exist_ok=True)
            repo_url = "git@gitlab.alibaba-inc.com:yocopen/%s.git" % component.name
            git2 = GitRepo(tmp1, repo_url)
            git = git2.repo.git
            git.pull('--progress', '--no-rebase', 'origin', 'master')
            git.checkout('master')
            # git@gitee.com:yocop/aos.git
            tmp2 = os.path.join('/tmp/yoc/gitee', component.name)
            if os.path.exists(tmp2):
                shutil.rmtree(tmp2)
            os.makedirs(tmp2, exist_ok=True)
            repo_url = "git@gitee.com:yocop/%s.git" % component.name
            git2 = GitRepo(tmp2, repo_url)
            git = git2.repo.git
            git.pull('--progress', '--no-rebase', 'origin', 'master')
            git.checkout('master')
            del_files_under_dir(tmp2, [".git"])
            copy_files_under_dir(tmp1, tmp2, [".git"])
            git.add(".")
            git.commit("-m", "update to %s." % new_tag)
            git.push('--set-upstream', 'origin', 'master')
            # push tag
            _push_tag(git, new_tag)
            return True
        except Exception as e:
            put_string(str(e), level='warning')
            if str(e).find("nothing to commit, working tree clean") > 0:
                try:
                    _push_tag(git, new_tag)
                    return True
                except Exception as e:
                    put_string(str(e), level='error')

    def merge_branch(self, from_branch, to_branch, component, shell_file, execute_shell):
        def _execute_shell_and_commit(git, to_branch, func, arg1, arg2):
            if func and func(arg1, arg2):
                try:
                    git.add(".")
                    git.commit("-m", "execute publish.")
                    git.push('--progress', 'origin', to_branch)
                except Exception as e:
                    put_string(str(e), level='error')
                    exit(0)
                else:
                    put_string("Commit publish ok.")

        git = self.repo.git
        try:
            git.checkout(from_branch)
            git.pull('--progress', '--no-rebase', 'origin', from_branch)
            #########################
            # backup from_branch repo
            tmp_path = os.path.join('/tmp/yoc/merge', component.name)
            if os.path.exists(tmp_path):
                shutil.rmtree(tmp_path)
            shutil.copytree(self.path, tmp_path, ignore=shutil.ignore_patterns("*.git"))
            #########################
            git.checkout(to_branch)
            git.pull('--progress', '--no-rebase', 'origin', to_branch)
            git.merge(from_branch)
            git.push('--progress', 'origin', to_branch)
        except Exception as ex:
            put_string(str(ex), level='warning')
            if str(ex).find("cmdline: git merge %s" % from_branch) > 0:
                put_string("Merge branch failed in %s. I will help you merge by automatic. Pleas wait..." % component.name)
                #########################
                try:
                    del_files_under_dir(self.path, [".git"])
                    copy_files_under_dir(tmp_path, self.path, [".git"])
                    git.add(".")
                    git.commit("-m", "merge from %s" % from_branch)
                    git.push('--progress', 'origin', to_branch)
                except Exception as ex:
                    put_string(str(ex), level='error')
                    return False
                else:
                    put_string("merge ok2.")
                    _execute_shell_and_commit(git, to_branch, execute_shell, component, shell_file)
                    return True
                #########################
            return False
        put_string("merge ok.")
        _execute_shell_and_commit(git, to_branch, execute_shell, component, shell_file)
        return True
    
    def checkout_branch(self, branch):
        git = self.repo.git
        try:
            git.pull('--progress', '--no-rebase', 'origin', branch)
            git.checkout(branch)
        except Exception as ex:
            put_string(str(ex), level='error')
            return False
        return True

    def push_tag(self, new_tag):
        git = self.repo.git
        try:
            local_tags = git.tag()
            if new_tag in local_tags:
                put_string("Need del local tag %s." % new_tag)
                git.tag("-d", new_tag)
            git.tag(new_tag)
            git.push('origin', "%s:refs/tags/%s" % (new_tag, new_tag))
        except Exception as ex:
            put_string(str(ex), level='error')
            return False
        return True