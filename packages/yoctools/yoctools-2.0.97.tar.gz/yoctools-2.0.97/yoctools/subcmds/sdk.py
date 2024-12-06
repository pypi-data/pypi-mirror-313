# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
import os
from yoctools import *


class Sdk(Command):
    common = True
    helpSummary = "Generate current solution SDK"
    helpUsage = """
%prog
"""
    helpDescription = """
generate current solution SDK.
"""
    def _Options(self, p):
        p.add_option('-b', '--board',
                     dest='board_name', action='store', type='str', default=None,
                     help='specify board name')
        p.add_option('-s', '--sdk',
                     dest='sdk_name', action='store', type='str', default=None,
                     help='specify chip sdk name')
        p.add_option('-u', '--update',
                     dest='update', action='store_true',
                     help='update package.yaml, Makefile, .gitignore files...')

    def Execute(self, opt, args):
        yoc = YoC()
        not_filter = not (opt.board_name or opt.sdk_name)
        solution = yoc.getSolution(board_name=opt.board_name, sdk_name=opt.sdk_name, not_filter=not_filter)
        if solution:
            solution.install()
            if opt.update:
                put_string("Update package.yaml, Makefile, .gitignore files...")
                pack = solution.solution_component.pack
                if pack:
                    for libname in solution.libs:
                        if libname not in pack.build_config.libs:
                            pack.build_config.libs.append(libname)

                    pack.build_config.libpath.append('yoc_sdk/lib')
                    pack.build_config.include.append('yoc_sdk/include')
                    pack.depends = {}
                    # pack.depends_forward = {}
                    pack.hw_info.reset()
                    pack.hw_info.cpu_name = solution.cpu_name
                    # pack.hw_info.ld_script = 'yoc_sdk/' + solution.ld_script_component.name + '/' + solution.ld_script_component.pack.hw_info.ld_script
                    # text = pack.dumps()
                    # print(text)
                    # copy and set ld file
                    ld_script_name = os.path.basename(solution.ld_script)
                    pack.hw_info.ld_script = ld_script_name
                    if os.path.dirname(solution.ld_script) != solution.solution_component.path:
                        shutil.copy2(solution.ld_script, pack.hw_info.ld_script)
                    put_string("Rebuilding package.yaml")
                    pack.defconfig.update(solution.org_defines)
                    pack.save(os.path.join(solution.solution_component.path, 'package.yaml'))
                    # Makefile
                    put_string("Rebuilding Makefile")
                    self.rebuild_makefile(solution.solution_component.path, 'Makefile')
                    # gitignore
                    put_string("Rebuilding .gitignore")
                    self.rebuild_gitignore(solution.solution_component.path, '.gitignore')
                    # .yoc
                    if not os.path.exists(os.path.join(os.getcwd(), '.yoc')):
                        conf = Configure()
                        shutil.copy2(os.path.join(conf.yoc_path, ".yoc"), os.getcwd())
            put_string("Generate %s SDK successful!" % solution.solution_component.name)
        else:
            put_string("No solution found in current directory!", level='warning')

    def rebuild_makefile(self, path, filename):
        filename2 = filename + '.new'
        filepath = os.path.join(path, filename)
        filepath2 = os.path.join(path, filename2)
        if os.path.isfile(filepath):
            with codecs.open(filepath, 'r', 'UTF-8') as f:
                with codecs.open(filepath2, 'w', 'UTF-8') as fn:
                    for line in f.readlines():
                        if "rm" in line and "yoc_sdk" in line:
                            fn.write("\t%s" % '$(CPRE) rm -rf out yoc.* generated/*.hex generated/*.zip\n')
                        else:
                            fn.write(line)
                    shutil.move(filepath2, filepath)

    def rebuild_gitignore(self, path, filename):
        filename2 = filename + '.new'
        filepath = os.path.join(path, filename)
        filepath2 = os.path.join(path, filename2)
        if os.path.isfile(filepath):
            with codecs.open(filepath, 'r', 'UTF-8') as f:
                with codecs.open(filepath2, 'w', 'UTF-8') as fn:
                    for line in f.readlines():
                        if "yoc_sdk" not in line and "generated" not in line:
                            fn.write(line)
                    shutil.move(filepath2, filepath)


