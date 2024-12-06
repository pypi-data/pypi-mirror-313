# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *
import os


class Rename(Command):
    common = True
    helpSummary = "Component rename <old_name> to <new_name>"
    helpUsage = """
%prog <old_name> <new_name>
"""
    helpDescription = """
Component rename <old_name> to <new_name>.
"""

    def Execute(self, opt, args):
        yoc = YoC()
        if len(args) == 2:
            old_name = args[0]
            new_name = args[1]
            if is_contain_chinese(new_name) or not is_legal_name(new_name):
                put_string("New name: %s is not valid!" % new_name, level='error')
                exit(-1)
            component = yoc.components.get(old_name)
            if component:
                if os.getcwd() == component.path:
                    put_string("Can't rename component in its own directory!", level='error')
                    exit(-1)
                dep_on = yoc.check_depend_on(component)
                if component.rename(new_name):
                    dep_on_list = []
                    for c in dep_on:
                        if c not in dep_on_list:
                            dep_on_list.append(c)
                        dep_on.extend(yoc.check_depend_on(c))
                    for c in dep_on_list:
                        dep_flag = False
                        for v in c.pack.depends:
                            if old_name in v:
                                c.pack.depends.remove(v)
                                dep_flag = True
                        # for v in c.pack.depends_forward:
                        #     if old_name in v:
                        #         c.pack.depends_forward.remove(v)
                        if dep_flag:
                            c.pack.depends.append({component.name: component.version})
                        if c.hw_info:
                            if c.hw_info.board_name == old_name:
                                c.pack.hw_info.merge_with_kv({"board_name": new_name})
                                dep_flag = True
                            if c.hw_info.chip_name == old_name:
                                c.pack.hw_info.merge_with_kv({"chip_name": new_name})
                                dep_flag = True
                        # c.pack.depends_forward.append({component.name: component.version})
                        if dep_flag:
                            c.pack.save(os.path.join(c.path, 'package.yaml'))
                            put_string("Component %s's package.yaml is upgraded." % c.name)
                    put_string("Component `%s` -> `%s` success." % (old_name, new_name))
                else:
                    put_string("Component rename fail!", level='warning')
            else:
                put_string("Component `%s` not found!" % old_name, level='warning')
        else:
            self.Usage()

