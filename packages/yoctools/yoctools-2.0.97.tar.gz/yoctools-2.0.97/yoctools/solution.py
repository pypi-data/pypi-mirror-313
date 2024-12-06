# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
import os
import re

from .log import logger
from .tools import *
from .package import *
from .component import *
from .builder import *

class Variables:
    def __init__(self):
        self.vars = {}
        pass

    def set(self, k, v, lower=False):
        self.vars[k] = v
        if lower:
            self.vars[k.lower()] = v.lower()

    def get(self, var):
        if var in self.vars:
            return self.vars[var]

    def convert(self, var):
        if var == None or len(var) == 0:
            return None

        v = var.split('?')
        if len(v) > 1:
            x = re.search('<(.+?)>', v[1], re.M | re.I)
            if x:
                x = self.get(x.group(1))
                if str(x) not in ['y', 'yes', 't', 'true', '1', True, 1]:
                    return None
                var = v[0].strip()

        x = re.findall('<(.+?)>', var)
        for key in x:
            value = self.get(key)
            if value != None:
                var = var.replace('<'+key+'>', self.vars[key])
            else:
                put_string('Not found variable:', var, level='warning')

        return var

    def items(self):
        return self.vars.items()


class Solution:
    def __init__(self, components, file_non_existent_no_err=False):
        self.variables = Variables()
        self.solution_component = None       # 当前 solution 组件
        self.board_component = None          # 当前开发板组件
        self.chip_component = None           # 当前芯片组件
        self.sdk_chip_component = None       # 当前芯片SDK组件
        self.components = components         # 使用到的组件
        self.global_includes = []
        self.libs = []
        self.libpath = []
        self.depend_libs = []
        self.external_libs = []
        self.external_libpath = []
        self.org_defines = {}
        self.defines = {}
        self.ASFLAGS = []
        self.CCFLAGS = []
        self.CXXFLAGS = []
        self.LINKFLAGS = []
        self.ld_script = ''
        self.ld_script_component = None
        self.cpu_name = ''
        self.toolchain_prefix = ''
        self.toolchain_path = ''
        self.algorithms_path = ''
        self.mkflash_script = ''

        # find current solution & board component
        for component in self.components:
            if component.path == os.getcwd() and component.type == 'solution':
                self.solution_component = component
                if self.solution_component.hw_info.board_name:
                    self.board_component = self.components.get(
                        self.solution_component.hw_info.board_name)
                    # sdk_chip
                    if not self.board_component:
                        put_string("Not found in `%s` components that the current project depends on. " %
                                   self.solution_component.hw_info.board_name, level='error')
                        exit(-1)

                    self.chip_component = self.components.get(
                        self.board_component.hw_info.chip_name)
                    if not self.chip_component:
                        put_string("Not found in `%s` components that the current project depends on. " %
                                   self.board_component.hw_info.chip_name, level='error')
                        exit(-1)
                elif self.solution_component.hw_info.chip_name:
                    self.chip_component = self.components.get(self.solution_component.hw_info.chip_name)
                    if not self.chip_component:
                        put_string("Not found in `%s` components that the current project depends on. " %
                                   self.board_component.hw_info.chip_name, level='error')
                        exit(-1)
                break

        if not self.solution_component:
            put_string('The current directory is not a solution directory.', level='error')
            exit(-1)

        if (not self.board_component) and (not self.solution_component.hw_info.cpu_name) and (not self.solution_component.hw_info.ld_script):
            for name in self.solution_component.depends:
                if type(name) == dict:
                    name = list(name.keys())[0]
                component = self.components.get(name)
                if component:
                    if component.type == 'board':
                        self.board_component = component
                        self.solution_component.hw_info.board_name = self.board_component.name
                        self.chip_component = self.components.get(
                            self.board_component.hw_info.chip_name)
                        if self.chip_component:
                            self.solution_component.hw_info.chip_name = self.chip_component.name
                        else:
                            put_string("Not found chip component: " +
                                       self.board_component.hw_info.chip_name, level='error')
                            exit(-1)
                        break
                else:
                    put_string("`%s` not found, please install it: yoc install %s" %
                               (name, name), level='error')
                    exit(-1)
            if not self.board_component:
                logger.warning(
                    'Not found board component in depends')

        if self.board_component:
            self.board_component.need_build = True
        if self.chip_component:
            self.chip_component.need_build = True

        components = ComponentGroup()
        for component in self.components:
            if component.need_build:
                components.add(component)
        self.components = components

        def cpu_set_variable(cpu, arch):
            def gen_cpu_defs(cpu):
                c = cpu.upper()
                c = c.replace('-', '').replace('.', '')
                c = '__CPU_' + c + '__'
                return c
            def gen_arch_defs(arch):
                a = arch.upper()
                a = '__ARCH_' + a + '__'
                return a

            self.cpu_name = cpu
            self.variables.set('CPU', cpu.upper(), True)
            if arch == '' or arch.upper() == 'CSKY':
                self.variables.set('cpu_num', cpu_id(cpu))
                self.variables.set('ARCH', 'CSKY', True)
            elif arch.upper() == 'ARM':
                self.variables.set('cpu_num', arm_cpu_id(cpu))
                self.variables.set('ARCH', arch, True)
            elif arch.upper() == 'RISCV':
                self.variables.set('cpu_num', riscv_cpu_id(cpu))
                self.variables.set('ARCH', arch, True)
            else:
                logger.error("not support arch:%s yet" % arch)
                exit(-1)
            # add cpu and arch defines,like __CPU_COTEXM0__ and __ARCH_ARM__
            # self.variables.set(gen_arch_defs(arch), 1)
            # self.variables.set(gen_cpu_defs(cpu), 1)

        def add_defines(component):
            for k, v in component.defconfig.items():
                self.variables.set(k, v)
                self.defines[k] = v
                self.org_defines[k] = v
        # copy defines
        for component in self.components:
            if component.type == 'common':
                add_defines(component)
        for component in self.components:
            if component.type == 'chip':
                add_defines(component)
        for component in self.components:
            if component.type == 'board':
                add_defines(component)
        for component in self.components:
            if component.type == 'solution':
                add_defines(component)

        solution_hw_info = HardwareInfo({})
        for component in [self.chip_component, self.board_component, self.solution_component]:
            if component:
                solution_hw_info.merge(component.hw_info)

                for c in component.build_config.cflag.split():
                    self.CCFLAGS.append(c)
                for c in component.build_config.asmflag.split():
                    self.ASFLAGS.append(c)
                for c in component.build_config.cxxflag.split():
                    self.CXXFLAGS.append(c)
                for c in component.build_config.ldflag.split():
                    self.LINKFLAGS.append(c)

        # pre/post script
        for component in [self.chip_component, self.board_component, self.solution_component]:
            if component:
                if component.build_config.prebuild_script:
                    self.solution_component.pre_scripts.append(os.path.join(component.path, component.build_config.prebuild_script))
                if component.build_config.postbuild_script:
                    self.solution_component.post_scripts.append(os.path.join(component.path, component.build_config.postbuild_script))

        # 根据 cpu_id 加载配置
        if len(solution_hw_info.cpu_list) != 0 and not solution_hw_info.cpu_id:
            put_string("Please set hw_info.cpu_id.", level='error')
            exit(-1)
        if solution_hw_info.cpu_id in solution_hw_info.cpu_list:
            for k, v in solution_hw_info.cpu_list[solution_hw_info.cpu_id].items():
                solution_hw_info.__dict__[k] = v

        # board 的hw_info 次优先
        if self.board_component and self.board_component.hw_info:
            solution_hw_info.merge(self.board_component.hw_info)
        # soution 的hw_info 优先
        solution_hw_info.merge(self.solution_component.hw_info)

        if solution_hw_info.cpu_name == '':
            put_string("Can't find cpu_name, please set cpu_name", level='error')
            exit(-1)

        if solution_hw_info.cpu_name:
            cpu_set_variable(solution_hw_info.cpu_name,
                             solution_hw_info.arch_name)

        if solution_hw_info.cpu_id:
            self.variables.set(solution_hw_info.cpu_id.upper(), True)

        if solution_hw_info.vendor_name:
            self.variables.set(
                'VENDOR', solution_hw_info.vendor_name.upper(), True)

        if solution_hw_info.chip_name:
            self.variables.set(
                'CHIP', solution_hw_info.chip_name.upper(), True)

        if solution_hw_info.board_name:
            self.variables.set(
                'BOARD', solution_hw_info.board_name.upper(), True)

        if solution_hw_info.flash_program:
            self.variables.set(
                'ALGORITHMS_PATH', solution_hw_info.flash_program)

        if self.chip_component:
            self.variables.set('CHIP_PATH', self.chip_component.path)

        if self.board_component:
            self.variables.set('BOARD_PATH', self.board_component.path)

        self.variables.set('SOLUTION_PATH', self.solution_component.path)
        self.yoc_path = os.path.join(self.solution_component.path, 'yoc_sdk')
        self.lib_path = os.path.join(self.yoc_path, 'lib')
        self.libpath.append(self.lib_path)

        self.global_includes.append(os.path.join(
            self.solution_component.path, 'include'))

        for component in self.components:
            if len(component.source_files) > 0 and component.name not in self.libs:
                self.libs.append(component.name)
                # if component.name is start with lib, scons will not add prefix: lib
                if component.name.startswith('lib'):
                    self.depend_libs.append(os.path.join(
                        self.lib_path, component.name + '.a'))
                else:
                    self.depend_libs.append(os.path.join(
                        self.lib_path, 'lib' + component.name + '.a'))

            component.variable_convert(self.variables, file_non_existent_no_err)

            # include
            for path in component.build_config.include:
                if path not in self.global_includes:
                    self.global_includes.append(path)

            # libpath
            for path in component.build_config.libpath:
                if path not in self.libpath:
                    self.libpath.append(path)
                if path not in self.external_libpath:
                    self.external_libpath.append(path)

            # libs
            for lib in component.build_config.libs:
                if lib not in self.libs:
                    self.libs.append(lib)
                if lib not in self.external_libs:
                    self.external_libs.append(lib)

        # external libs changed need to relink
        for lib in self.external_libs:
            for path in self.external_libpath:
                filename = os.path.join(path, 'lib' + lib + '.a')
                if os.path.exists(filename):
                    self.depend_libs.append(filename)
                    break

        self.toolchain_prefix = solution_hw_info.toolchain_prefix
        self.toolchain_path = solution_hw_info.toolchain_path
        self.ld_script = solution_hw_info.ld_script
        self.ld_script = self.variables.convert(self.ld_script)
        self.algorithms_path = solution_hw_info.flash_program
        self.algorithms_path = self.variables.convert(self.algorithms_path)
        if not self.algorithms_path:
            self.algorithms_path = ''

        if self.solution_component.hw_info.ld_script:
            self.ld_script_component = self.solution_component
        elif self.board_component and self.board_component.hw_info.ld_script:
            self.ld_script_component = self.board_component
        elif self.chip_component and self.chip_component.hw_info.ld_script:
            self.ld_script_component = self.chip_component
        elif self.chip_component and self.ld_script:
            # multi cpu
            self.ld_script_component = self.chip_component
        else:
            logger.error("not found LD script file, please set ld_script")
            exit(-1)

        self.mkflash_script = self.solution_component.mkflash_script
        self.mkflash_script = self.variables.convert(self.mkflash_script)

        # append variables to defines
        for k, v in self.variables.items():
            if k.isupper():
                if k.startswith('__CPU_') or k.startswith('__ARCH_'):
                    self.defines[k] = v

    def install(self):
        for component in self.components:
            component.install(self.yoc_path)

    def show(self, show_component=True, show_libs=True, show_include=True, show_define=True, show_veriable=True, show_flags=True):
        if show_component:
            put_string("[component]")
            for c in self.components:
                c.show(4)

            put_string()
            if self.solution_component:
                put_string("    solution component: " +
                           self.solution_component.name)
            if self.board_component:
                put_string("    board component   : " +
                           self.board_component.name)
            if self.chip_component:
                put_string("    chip component    : " +
                           self.chip_component.name)

        if show_libs:
            put_string("[libs]")
            for v in self.libs:
                put_string('    ' + v)

            put_string("[libpath]")
            for v in self.libpath:
                put_string('    ' + v)

        if show_include:
            put_string("[global_includes]")
            for v in self.global_includes:
                put_string('    ' + v)

        if show_define:
            put_string("[defines]")
            for k, v in self.defines.items():
                put_string('    ', k, '=', v)

        if show_veriable:
            put_string("[variables]")
            for k, v in self.variables.items():
                put_string('    %s = %s' % (k, v))

        if show_flags:
            build_env = Builder(self)
            for a in build_env.env['ASFLAGS']:
                if a not in self.ASFLAGS:
                    self.ASFLAGS.insert(0, a)
            for a in build_env.env['CCFLAGS']:
                if a not in self.CCFLAGS:
                    self.CCFLAGS.insert(0, a)
            for a in build_env.env['CXXFLAGS']:
                if a not in self.CXXFLAGS:
                    self.CXXFLAGS.insert(0, a)
            for a in build_env.env['LINKFLAGS']:
                if a not in self.LINKFLAGS:
                    self.LINKFLAGS.insert(0, a)
            put_string("ASMFLAGS  :" + ' '.join(self.ASFLAGS))
            put_string("CCFLAGS   :" + ' '.join(self.CCFLAGS))
            put_string("CXXFLAGS  :" + ' '.join(self.CXXFLAGS))
            put_string("LINKFLAGS :" + ' '.join(self.LINKFLAGS))
            put_string('ld_script : ' + self.ld_script)
            put_string('toolchain : ' + self.toolchain_prefix)
            put_string('toolchain_path : ' + self.toolchain_path)
            put_string('algorithms_path : ' + self.algorithms_path)


def cpu_id(s):
    s += 'z'
    ids = ''
    for c in s:
        if ord(c) >= ord('0') and ord(c) <= ord('9'):
            ids += c
        elif ids:
            return ids


def arm_cpu_id(s):
    if s.startswith('arm'):
        return s[3:]
    else:
        arr = s.split('-')
        if len(arr) > 1:
            return arr[1]

def riscv_cpu_id(cpu):
    a = cpu.lower()
    if a == 'rv32emc' or a == 'rv32ec' or a == 'rv32i' or a == 'rv32iac' \
        or a == 'rv32im' or a == 'rv32imac' or a == 'rv32imafc':
        return 'rv32'
    elif a == 'e902' or a == 'e902m' or a == 'e902t' or a == 'e902mt':
        return 'rv32_16gpr'
    elif a == 'e906' or a == 'e906p' or a == 'e907' or a == 'e907p' or a == 'c907-rv32':
        return 'rv32_32gpr'
    elif a == 'e907f' or a == 'e907fp' or a == 'e906f' or a == 'e906fp':
        return 'rv32f_32gpr'
    elif a == 'e906fd' or a == 'e906fdp' or a == 'e907fd' or a == 'e907fdp' or a == 'c907fd-rv32' or a == 'c907fdv-rv32' or a == 'c907fdvm-rv32':
        return 'rv32fd_32gpr'
    elif a == 'c906' or a == 'c908i' or a == 'c907':
        return 'rv64_32gpr'
    elif a == 'c906fd' or a == 'c906fdv' \
        or a == 'c907fd' or a == 'c907fdv' or a == 'c907fdvm' \
        or a == 'c908' or a == 'c908v' \
        or a == 'c910' or a == 'c910v2' or a == 'c910v3' or a == 'c910v3-cp' \
        or a == 'c920' or a == 'c920v2' or a == 'c920v3' or a ==  'c920v3-cp' or a == 'c920v3-ant' \
        or a == 'r910' or a == 'r920' \
        or a == 'r908' or a == 'r908fd' or a == 'r908fdv' or a == 'r908-cp' or a == 'r908fd-cp' or a == 'r908fdv-cp':
        return 'rv64fd_32gpr'
    else:
        put_string("%s not support yet." % a, level='error')
        exit(0)
