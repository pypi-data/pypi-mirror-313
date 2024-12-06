# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited

from __future__ import print_function
from yoctools import *

import codecs
import shutil
import csv

rv_cpus = []
platforms = []
kernels = []

class Cds(Command):
    common = True
    helpSummary = "Generate current solution CDS project"
    helpUsage = """
%prog [cpu] [platfrom] [kernel] [options]
"""
    helpDescription = """
generate current solution CDS project.
"""

    def _Options(self, p):
        p.add_option('-f', '--file',
                     dest='file', action='store', type='str', default=None,
                     help='the xt_rtos_sdk.csv file path')
        p.add_option('-s', '--solution',
                            dest='solution', action='store', type='str', default=None,
                            help='specify the solution name when use csv file to build cds project. If there are multiple solutions, please separate them with commas')
        p.add_option('-p', '--platform',
                            dest='platform', action='store', type='str', default=None,
                            help='specify the platform when use csv file to build cds project, If there are multiple platforms, please separate them with commas')
        p.add_option('-k', '--kernel',
                            dest='kernel', action='store', type='str', default=None,
                            help='specify the kernel when use csv file to build cds project, If there are multiple kernels, please separate them with commas')
        p.add_option('-c', '--cpu',
                    dest='cpu', action='store', type='str', default=None,
                    help='specify the cpu when use csv file to build cds project, If there are multiple cpus, please separate them with commas')
        p.add_option('-d', '--sdk',
                     dest='sdk_name', action='store', type='str', default=None,
                     help='specify chip sdk name, except dummy project.')

    def Execute(self, opt, args):
        cpu = platform = kernel = None
        if len(args) > 0:
            cpu = args[0]
        if len(args) > 1:
            platform = args[1]
        if len(args) > 2:
            kernel = args[2]

        if (opt.file and opt.sdk_name) or (cpu and opt.sdk_name) or (cpu and opt.file):
            put_string("Please input the right options.", level='warning')
            exit(1)

        global rv_cpus
        global platforms
        global kernels
        rv_cpus = globals()['RiscvCPU']
        platforms = globals()['xt_platforms']
        kernels = globals()['xt_kernels']

        def _build_cds_proj(cpu, platform, kernel):
            if cpu:
                if not platform:
                    put_string("Please input the platform argument.", level='warning')
                    exit(1)
                put_string("Building [%s/%s/%s] cds project files, please wait..." % (cpu, platform, kernel))
            elif opt.sdk_name:
                put_string("Building [%s] cds project files, please wait..." % opt.sdk_name)
            else:
                put_string("Building cds project files, please wait...")
            put_string(os.getcwd())

            if cpu and (cpu not in rv_cpus):
                put_string("The cpu [%s] is not support yet!" % cpu, level='warning')
                put_string(rv_cpus)
                exit(1)
            if platform and (platform not in platforms):
                put_string("The platform [%s] is not support yet!" % platform, level='warning')
                put_string(platforms)
                exit(1)
            if kernel and (kernel not in kernels):
                put_string("The kernel [%s] is not support yet!" % kernel, level='warning')
                put_string(kernels)
                exit(1)

            if cpu:
                solution_packyaml = os.path.join(os.getcwd(), 'package.yaml')
                if not os.path.isfile(solution_packyaml):
                    put_string("Can't find %s file." % solution_packyaml, level='warning')
                    exit(1)
                is_have_sdkchip = False
                pack = Package(solution_packyaml)
                if pack.type != 'solution':
                    put_string("The current directory is not a solution!!!", level='warning')
                    exit(1)
                for d in pack.depends:
                    if 'sdk_chip_riscv_dummy' in d.keys():
                        is_have_sdkchip = True
                        break
                if is_have_sdkchip and not kernel:
                    put_string("Please input the kernel argument.", level='warning')
                    exit(1)
                chip_comp = os.path.join(os.getcwd(), '../../components/chip_riscv_dummy')
                board_comp = os.path.join(os.getcwd(), '../../boards/board_riscv_dummy')
                sdkchip_comp = os.path.join(os.getcwd(), '../../components/sdk_chip_riscv_dummy')
                chip_yaml_file = os.path.join(chip_comp, "package.yaml")
                chip_yaml_file_bak = os.path.join(chip_comp, "package.yaml" + ".bak")
                board_yaml_file = os.path.join(board_comp, "package.yaml")
                board_yaml_file_bak = os.path.join(board_comp, "package.yaml" + ".bak")
                sdkchip_yaml_file = os.path.join(sdkchip_comp, "package.yaml")
                sdkchip_yaml_file_bak = os.path.join(sdkchip_comp, "package.yaml" + ".bak")
                solution_yaml_file = os.path.join(os.getcwd(), "package.yaml")
                solution_yaml_file_bak = os.path.join(os.getcwd(), "package.yaml" + ".bak")
                build_chip_yaml_file = os.path.join(chip_comp, "package.yaml." + cpu)
                build_board_yaml_file = os.path.join(board_comp, "package.yaml." + platform)
                build_sdkchip_yaml_file = ''
                if kernel:
                    build_sdkchip_yaml_file = os.path.join(sdkchip_comp, "package.yaml." + kernel)
                build_solution_yaml_file = os.path.join(os.getcwd(), "package.yaml." + cpu)
                build_solution_yaml_file2 = os.path.join(os.getcwd(), "package.yaml." + platform)
                if os.path.isfile(build_chip_yaml_file):
                    shutil.copy2(chip_yaml_file, chip_yaml_file_bak)
                    shutil.copy2(build_chip_yaml_file, chip_yaml_file)
                if os.path.isfile(build_board_yaml_file):
                    shutil.copy2(board_yaml_file, board_yaml_file_bak)
                    shutil.copy2(build_board_yaml_file, board_yaml_file)
                if os.path.isfile(build_sdkchip_yaml_file) and is_have_sdkchip:
                    shutil.copy2(sdkchip_yaml_file, sdkchip_yaml_file_bak)
                    shutil.copy2(build_sdkchip_yaml_file, sdkchip_yaml_file)
                if os.path.isfile(build_solution_yaml_file) or os.path.isfile(build_solution_yaml_file2):
                    if os.path.isfile(build_solution_yaml_file):
                        shutil.copy2(solution_yaml_file, solution_yaml_file_bak)
                        shutil.copy2(build_solution_yaml_file, solution_yaml_file)
                    else:
                        shutil.copy2(solution_yaml_file, solution_yaml_file_bak)
                        shutil.copy2(build_solution_yaml_file2, solution_yaml_file)

            def _clean_backup_file():
                if cpu:
                    try:
                        if os.path.isfile(chip_yaml_file_bak):
                            shutil.copy2(chip_yaml_file_bak, chip_yaml_file)
                            os.remove(chip_yaml_file_bak)
                        if os.path.isfile(board_yaml_file_bak):
                            shutil.copy2(board_yaml_file_bak, board_yaml_file)
                            os.remove(board_yaml_file_bak)
                        if os.path.isfile(sdkchip_yaml_file_bak):
                            shutil.copy2(sdkchip_yaml_file_bak, sdkchip_yaml_file)
                            os.remove(sdkchip_yaml_file_bak)
                        if os.path.isfile(solution_yaml_file_bak):
                            shutil.copy2(solution_yaml_file_bak, solution_yaml_file)
                            os.remove(solution_yaml_file_bak)
                    except Exception as ex:
                        put_string(str(ex), level='warning')
                        exit(1)

            yoc = YoC()
            solution = yoc.getSolution(sdk_name=opt.sdk_name, file_non_existent_no_err=True)
            if not solution:
                put_string("The current directory is not a solution!", level='warning')
                _clean_backup_file()
                exit(1)
            if opt.sdk_name:
                put_string(solution.board_component.name, solution.chip_component.name)
            # elif solution.chip_component.name != 'chip_riscv_dummy':
            #     put_string("Not support this project yet!", level='warning')
            #     _clean_backup_file()
            #     exit(1)
            if cpu and cpu != solution.cpu_name:
                put_string("The cpu name is not match, please check!", level='warning')
                _clean_backup_file()
                exit(1)

            cds_proj_dir = os.path.join(os.getcwd(), 'cds')
            if not os.path.exists(cds_proj_dir):
                os.makedirs(cds_proj_dir)
            cds_proj_path_depth = 3
            if opt.sdk_name:
                cds_proj_path_depth = cds_proj_path_depth + 1
                cds_proj_dir = os.path.join(cds_proj_dir, opt.sdk_name)
            if cpu:
                cds_proj_path_depth = cds_proj_path_depth + 1
                cds_proj_dir = os.path.join(cds_proj_dir, cpu)
            if platform:
                cds_proj_path_depth = cds_proj_path_depth + 1
                cds_proj_dir = os.path.join(cds_proj_dir, platform)
            if kernel:
                cds_proj_path_depth = cds_proj_path_depth + 1
                cds_proj_dir = os.path.join(cds_proj_dir, kernel)
            if not os.path.exists(cds_proj_dir):
                os.makedirs(cds_proj_dir)
            if not os.path.exists(cds_proj_dir):
                put_string("The cds dir %s is not exist, makedirs failed!" % cds_proj_dir, level='warning')
                _clean_backup_file()
                exit(1)
            # print('cds_proj_path_depth', cds_proj_path_depth)

            # print(solution.solution_component.name)
            mk = Make('cds_proj_gen', sdkname = opt.sdk_name)
            mk.build_components()
            # print(mk.build_env.cds_cfgs)

            files = mk.build_env.cds_cfgs['sources']
            includes = mk.build_env.cds_cfgs['CPPPATH']
            cppdefines = mk.build_env.cds_cfgs['CPPDEFINES']
            cflags_o = mk.build_env.cds_cfgs['CFLAGS']
            cxxflags_o = mk.build_env.cds_cfgs['CXXFLAGS']
            asflags_o = mk.build_env.cds_cfgs['ASFLAGS']
            linkflags_o = mk.build_env.cds_cfgs['LINKFLAGS']
            # remove -mcpu
            cflags = []
            for e in cflags_o:
                if not e.startswith("-mcpu="):
                    cflags.append(e)
            cxxflags = []
            for e in cxxflags_o:
                if not e.startswith("-mcpu="):
                    cxxflags.append(e)
            asflags = []
            for e in asflags_o:
                if not e.startswith("-mcpu="):
                    asflags.append(e)
            linkflags = []
            for e in linkflags_o:
                if not e.startswith("-mcpu="):
                    linkflags.append(e)

            left_fill_space = 36
            cpu_type_base_str = 'ckcoregcc.default.CPUType.'

            yoc_base_path = yoc.yoc_path
            # .project file
            link_txts = ''
            files.append(solution.ld_script)
            link_path_base = 'PARENT-' + str(cds_proj_path_depth) + '-PROJECT_LOC/'
            for f in files:
                filename = os.path.relpath(f, yoc_base_path)
                filepath = link_path_base + filename
                lt = link_template.format(
                    link_file_name = filename,
                    link_file_path = filepath
                )
                link_txts += lt
            link_txts += '\n'
            project_content = project_template.format(
                name = solution.solution_component.name,
                link_content = link_txts
            )
            # print(project_content)

            # .cproject file
            # macro defines
            defined_txts = ''
            defined_template = '''<listOptionValue builtIn="false" value="{defined_sym}"/>'''
            for d in cppdefines:
                if len(d) > 1:
                    d1 = d[1]
                    if type(d1) == str and d1 == '\\"y\\"':
                        ds = d[0]
                    elif type(d1) == str:
                        d1 = d1.replace('\\"', '&quot;')
                        ds = '{}={}'.format(d[0], d1)
                    else:
                        ds = '{}={}'.format(d[0], d1)
                else:
                    ds = d[0]
                defineds = defined_template.format(
                    defined_sym = ds
                )
                defined_txts += defineds.rjust(left_fill_space + len(defineds)) + '\n'
            defined_txts = defined_txts[:-1]
            # print(defined_txts)

            # includes
            include_template = '''<listOptionValue builtIn="false" value="{include_path}"/>'''
            includes_txts = ''
            inlcude_base_path = ''
            for i in range(0, cds_proj_path_depth + 1):
                inlcude_base_path = inlcude_base_path + "../"
            for i in includes:
                include = '&quot;' + inlcude_base_path + os.path.relpath(i, yoc_base_path) + '&quot;'
                include_txt = include_template.format(
                    include_path = include
                )
                includes_txts += include_txt.rjust(left_fill_space + len(include_txt)) + '\n'
            includes_txts = includes_txts[:-1]

            cpu_type_str = cpu_type_base_str + solution.cpu_name
            # print(cpu_type_str)

            # libs path
            # print("external_libpath:", solution.external_libpath)
            lib_path_template = '''<listOptionValue builtIn="false" value="{lib_path}"/>'''
            libpath_txts = ''
            for l in solution.external_libpath:
                lpath = '&quot;' + inlcude_base_path + os.path.relpath(l, yoc_base_path) + '&quot;'
                libpath_txt = lib_path_template.format(
                    lib_path = lpath
                )
                libpath_txts += libpath_txt.rjust(left_fill_space + len(libpath_txt)) + '\n'
            libpath_txts = libpath_txts[:-1]

            # libs
            # print("external_libs:", solution.external_libs)
            exlibs = solution.external_libs
            # exlibs.extend(['m', 'gcc'])
            libs_template = '''<listOptionValue builtIn="false" value="{libs_var}"/>'''
            libs_txts = ''
            for l in exlibs:
                libs_txt = libs_template.format(
                    libs_var = l
                )
                libs_txts += libs_txt.rjust(left_fill_space + len(libs_txt)) + '\n'
            libs_txts = libs_txts[:-1]

            otherflags = ["-c"]
            othercppflags = ["-c"]
            for f in cflags:
                if f not in otherflags:
                    otherflags.append(f)
            for f in cxxflags:
                if f not in othercppflags:
                    othercppflags.append(f)
            # print("otherflags:", otherflags)

            sbc_base_path = ''
            for i in range(0, cds_proj_path_depth):
                sbc_base_path = sbc_base_path + "../"
            cproject_content = cproject_template.format(
                postbuildStep_var = "sh ${PWD}/../aft_build.sh ${ProjName} ${SolutionPath} ${BoardPath} ${ChipPath}",
                asm_flags_var = '-c ' + ' '.join(asflags),
                linker_flags_var = ' '.join(linkflags),
                defined_symbols_list = defined_txts,
                includes_list = includes_txts,
                cpu_type_str = cpu_type_str,
                libpath_list = libpath_txts,
                libs_list = libs_txts,
                linker_script_path = inlcude_base_path + os.path.relpath(solution.ld_script, yoc.yoc_path),
                other_cppflags = ' '.join(othercppflags),
                other_flags = ' '.join(otherflags),
                solution_path = "${ProjDirPath}/" + sbc_base_path + "solutions/" + solution.solution_component.name,
                board_path = "${ProjDirPath}/" + sbc_base_path + "boards/" + solution.board_component.name,
                chip_path = "${ProjDirPath}/" + sbc_base_path + "components/" + solution.chip_component.name
            )
            # print(cproject_content)

            aft_build_content = aft_script_template

            # generate cds project files
            try:
                filename = os.path.join(solution.solution_component.path, os.path.join(cds_proj_dir, '.project'))
                with codecs.open(filename, 'w', 'UTF-8') as f:
                    if sys.version_info.major == 2:
                        if type(project_content) == str:
                            project_content = project_content.decode('UTF-8')
                    f.write(project_content)
                    put_string("Generate cds .project file success.", level='info')
            except Exception as ex:
                put_string("Generate %s file failed." % filename, level='warning')
                _clean_backup_file()
                exit(1)

            try:
                filename = os.path.join(solution.solution_component.path, os.path.join(cds_proj_dir, '.cproject'))
                with codecs.open(filename, 'w', 'UTF-8') as f:
                    if sys.version_info.major == 2:
                        if type(cproject_content) == str:
                            cproject_content = cproject_content.decode('UTF-8')
                    f.write(cproject_content)
                    put_string("Generate cds .cproject file success.", level='info')
            except Exception as ex:
                put_string("Generate %s file failed." % filename, level='warning')
                _clean_backup_file()
                exit(1)
            
            try:
                filename = os.path.join(solution.solution_component.path, os.path.join(cds_proj_dir, 'aft_build.sh'))
                with codecs.open(filename, 'w', 'UTF-8') as f:
                    if sys.version_info.major == 2:
                        if type(aft_build_content) == str:
                            aft_build_content = aft_build_content.decode('UTF-8')
                    f.write(aft_build_content)
                    put_string("Generate cds aft_build.sh file success.", level='info')
            except Exception as ex:
                put_string("Generate %s file failed." % filename, level='warning')
                _clean_backup_file()
                exit(1)

            try:
                global gitignore_txt
                filename = os.path.join(solution.solution_component.path, os.path.join(cds_proj_dir, '.gitignore'))
                with codecs.open(filename, 'w', 'UTF-8') as f:
                    if sys.version_info.major == 2:
                        if type(gitignore_txt) == str:
                            gitignore_txt = gitignore_txt.decode('UTF-8')
                    f.write(gitignore_txt)
                    put_string("Generate cds .gitignore file success.", level='info')
            except Exception as ex:
                put_string("Generate %s file failed.(%s)" % (filename, str(ex)), level='warning')
                _clean_backup_file()
                exit(1)

            _clean_backup_file()
            put_string("Generate cds project at [%s] success." % cds_proj_dir, level='info')

        if opt.file:
            csv_file = os.path.realpath(opt.file)
            if not os.path.isfile(csv_file):
                put_string("Please check the file %s is exists." % csv_file, level='warning')
                exit(1)
            put_string("Use %s file to build all cds projects." % csv_file)
            yoc = YoC()
            specify_solution_list = []
            specify_platform_list = []
            specify_kernel_list = []
            specify_cpu_list = []
            if opt.solution:
                specify_solution_list = opt.solution.split(",")
                put_string(specify_solution_list)
            else:
                solution = yoc.getSolution()
                if solution:
                    specify_solution_list.append(solution.solution_component.name)
            if opt.platform:
                specify_platform_list = opt.platform.split(',')
                put_string(specify_platform_list)
            if opt.kernel:
                specify_kernel_list = opt.kernel.split(',')
                put_string(specify_kernel_list)
            if opt.cpu:
                specify_cpu_list = opt.cpu.split(',')
                put_string(specify_cpu_list)
            try:
                with codecs.open(csv_file, 'r', 'UTF-8') as f:
                    csvreader = csv.reader(f)
                    cnt = 0
                    for row in csvreader:
                        if len(row) == 0:
                            continue
                        #skip first line
                        if cnt != 0:
                            sname = row[0].strip()
                            cpu_list = [word.strip() for word in row[1].split('/')]
                            # cds_Y_N = row[2].strip()
                            # print(sname, specify_solution_list)
                            if len(specify_solution_list) > 0 and (sname not in specify_solution_list):
                                continue
                            # if cds_Y_N == 'N':
                            #     put_string("No need to build cds for %s." % sname, color='blue')
                            #     continue
                            def _build_with_csv():
                                sol = os.path.join(yoc.yoc_path, "solutions", sname)
                                if not os.path.exists(sol):
                                    put_string("%s not found, please check." % sol, level='warning')
                                    return
                                os.chdir(sol)
                                for c in cpu_list:
                                    cpu = c
                                    if opt.cpu and (cpu not in specify_cpu_list):
                                        continue
                                    platform = 'xiaohui'
                                    if c.startswith("e"):
                                        platform = 'smartl'
                                    if len(specify_platform_list) > 0 and (platform not in specify_platform_list):
                                        continue
                                    # print(sname, cpu, platform, kernel)
                                    try:
                                        _build_cds_proj(cpu, platform, kernel)
                                    except Exception as ex:
                                        put_string(str(ex), level='warning')
                                        exit(1)
                            if sname != 'solutions':
                                if sname.startswith('soc_'):
                                    # soc_xx demo support multi type kernel
                                    for k in kernels:
                                        kernel = k
                                        if len(specify_kernel_list) > 0 and (kernel not in specify_kernel_list):
                                            continue
                                        _build_with_csv()
                                else:
                                    kernel = None
                                    _build_with_csv()
                        cnt += 1
                exit(1)
            except Exception as ex:
                put_string("Read %s file failed.(%s)" % (csv_file, str(ex)), level='warning')
                exit(1)

        try:
            _build_cds_proj(cpu, platform, kernel)
        except Exception as ex:
            put_string(str(ex), level='warning')
            exit(1)

gitignore_txt = '''
/Debug/
/Release/
/boards/
/components/
/solutions/
%SystemDrive%
'''

project_template = '''<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
    <name>{name}</name>
    <comment></comment>
    <projects>
    </projects>
    <buildSpec>
        <buildCommand>
            <name>org.eclipse.cdt.managedbuilder.core.genmakebuilder</name>
            <triggers>clean,full,incremental,</triggers>
            <arguments>
            </arguments>
        </buildCommand>
        <buildCommand>
            <name>org.eclipse.cdt.managedbuilder.core.ScannerConfigBuilder</name>
            <triggers>full,incremental,</triggers>
            <arguments>
            </arguments>
        </buildCommand>
    </buildSpec>
    <natures>
        <nature>org.eclipse.cdt.core.cnature</nature>
        <nature>org.eclipse.cdt.core.ccnature</nature>
        <nature>org.eclipse.cdt.managedbuilder.core.managedBuildNature</nature>
        <nature>org.eclipse.cdt.managedbuilder.core.ScannerConfigNature</nature>
    </natures>
    <linkedResources>
        {link_content}
    </linkedResources>
</projectDescription>
'''

link_template = '''
        <link>
            <name>{link_file_name}</name>
            <type>1</type>
            <locationURI>{link_file_path}</locationURI>
        </link>'''

cproject_template = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?fileVersion 4.0.0?>
<cproject storage_type_id="org.eclipse.cdt.core.XmlProjectDescriptionStorage">
	<storageModule moduleId="org.eclipse.cdt.core.settings">
		<cconfiguration id="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.debug.210845159">
			<storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.debug.210845159" moduleId="org.eclipse.cdt.core.settings" name="Debug">
				<macros>
					<stringMacro name="ChipPath" type="VALUE_TEXT" value="{chip_path}"/>
					<stringMacro name="BoardPath" type="VALUE_TEXT" value="{board_path}"/>
					<stringMacro name="SolutionPath" type="VALUE_TEXT" value="{solution_path}"/>
				</macros>
                <externalSettings/>
				<extensions>
					<extension id="com.csky.cds.debug.core.RISCV64_ELF" point="org.eclipse.cdt.core.BinaryParser"/>
					<extension id="org.eclipse.cdt.core.GmakeErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
					<extension id="org.eclipse.cdt.core.CWDLocator" point="org.eclipse.cdt.core.ErrorParser"/>
					<extension id="org.eclipse.cdt.core.GCCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
					<extension id="org.eclipse.cdt.core.GASErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
					<extension id="org.eclipse.cdt.core.GLDErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
				</extensions>
			</storageModule>
			<storageModule moduleId="cdtBuildSystem" version="4.0.0">
				<configuration artifactName="${{ProjName}}" buildArtefactType="org.eclipse.cdt.build.core.buildArtefactType.exeWithoutOs" buildProperties="org.eclipse.cdt.build.core.buildArtefactType=org.eclipse.cdt.build.core.buildArtefactType.exeWithoutOs,org.eclipse.cdt.build.core.buildType=org.eclipse.cdt.build.core.buildType.debug" cleanCommand="rm -rf" description="" id="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.debug.210845159" name="Debug" parent="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.debug" postbuildStep="{postbuildStep_var}">
					<folderInfo id="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.debug.210845159." name="/" resourcePath="">
						<toolChain id="cds.managedbuild.toolchain.ckcoregcc.riscv64.exeWithoutOs.debug.1303157388" name="RISCV64 Elf ToolChain" superClass="cds.managedbuild.toolchain.ckcoregcc.riscv64.exeWithoutOs.debug">
							<targetPlatform archList="all" binaryParser="com.csky.cds.debug.core.RISCV64_ELF" id="cds.managedbuild.target.csky.platform.ckcoregcc.base.riscv64.1667937565" name="Debug Platform" osList="win32,linux,uclinux" superClass="cds.managedbuild.target.csky.platform.ckcoregcc.base.riscv64"/>
							<builder buildPath="${{workspace_loc:/fsafd}}/Debug" id="cds.managedbuild.target.ckcoregcc.builder.base.riscv64.114717048" keepEnvironmentInBuildfile="false" managedBuildOn="true" name="Gnu Make Builder" superClass="cds.managedbuild.target.ckcoregcc.builder.base.riscv64"/>
							<tool id="cds.managedbuild.tool.ckcoregcc.default.base.elf.riscv64.1366075186" name="All Tools Settings" superClass="cds.managedbuild.tool.ckcoregcc.default.base.elf.riscv64">
								<option id="cds.managedbuild.option.ckcoregcc.default.riscv64.cputype.1808119505" name="CPUType" superClass="cds.managedbuild.option.ckcoregcc.default.riscv64.cputype" value="{cpu_type_str}" valueType="enumerated"/>
							</tool>
							<tool id="cds.managedbuild.tool.ckcoregcc.assembler.base.elf.riscv64.912544459" name="CSky Elf Assembler" superClass="cds.managedbuild.tool.ckcoregcc.assembler.base.elf.riscv64">
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.assembler.option.def.symbols.1326843304" name="Defined symbols (-D)" superClass="ckcoregcc.assembler.option.def.symbols" useByScannerDiscovery="false" valueType="definedSymbols">
{defined_symbols_list}
								</option>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.both.asm.option.include.paths.149232132" name="Include paths (-I)" superClass="ckcoregcc.both.asm.option.include.paths" valueType="includePath">
{includes_list}
								</option>
                                <option id="ckcoregcc.both.asm.option.flags.1011966450" name="Assembler Flags" superClass="ckcoregcc.both.asm.option.flags" value="{asm_flags_var}" valueType="string"/>
								<inputType id="cds.managedbuild.tool.ckcoregcc.assembler.input2.1963154724" superClass="cds.managedbuild.tool.ckcoregcc.assembler.input2"/>
								<inputType id="cds.managedbuild.tool.ckcoregcc.assembler.input1.245242782" superClass="cds.managedbuild.tool.ckcoregcc.assembler.input1"/>
							</tool>
							<tool id="cds.managedbuild.tool.ckcoregcc.cpp.compiler.base.elf.riscv64.1176686421" name="CSky Elf C++ Compiler" superClass="cds.managedbuild.tool.ckcoregcc.cpp.compiler.base.elf.riscv64">
								<option id="ckcoregcc.cpp.compiler.option.optimization.level.2123175793" name="Optimization Level" superClass="ckcoregcc.cpp.compiler.option.optimization.level" value="Optimize size (-Os)" valueType="enumerated"/>
								<option id="ckcoregcc.cpp.compiler.option.debugging.level.1289480744" name="Debug Level" superClass="ckcoregcc.cpp.compiler.option.debugging.level" value="ckcoregcc.cpp.compiler.debugging.level.max" valueType="enumerated"/>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.cpp.compiler.option.preprocessor.def.591104318" name="Defined symbols (-D)" superClass="ckcoregcc.cpp.compiler.option.preprocessor.def" valueType="definedSymbols">
{defined_symbols_list}
								</option>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.cpp.compiler.option.include.paths.1896233795" name="Include paths (-I)" superClass="ckcoregcc.cpp.compiler.option.include.paths" valueType="includePath">
{includes_list}
								</option>
                                <option id="ckcoregcc.cpp.compiler.option.other.riscv64.other.1518412211" name="Other flags" superClass="ckcoregcc.cpp.compiler.option.other.riscv64.other" value="{other_cppflags}" valueType="string"/>
								<inputType id="cds.managedbuild.tool.ckcoregcc.cpp.compiler.input.1298562960" superClass="cds.managedbuild.tool.ckcoregcc.cpp.compiler.input"/>
							</tool>
							<tool id="cds.managedbuild.tool.ckcoregcc.c.compiler.base.elf.riscv64.1468555868" name="CSky Elf C Compiler" superClass="cds.managedbuild.tool.ckcoregcc.c.compiler.base.elf.riscv64">
								<option id="ckcoregcc.c.compiler.option.optimization.level.628002517" name="Optimization Level" superClass="ckcoregcc.c.compiler.option.optimization.level" value="Optimize size (-Os)" valueType="enumerated"/>
								<option id="ckcoregcc.c.compiler.option.debugging.level.34746961" name="Debug Level" superClass="ckcoregcc.c.compiler.option.debugging.level" value="ckcoregcc.c.compiler.debugging.level.max" valueType="enumerated"/>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.c.compiler.option.preprocessor.def.231204495" name="Defined symbols (-D)" superClass="ckcoregcc.c.compiler.option.preprocessor.def" useByScannerDiscovery="false" valueType="definedSymbols">
{defined_symbols_list}
								</option>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.c.compiler.option.include.paths.117613518" name="Include paths (-I)" superClass="ckcoregcc.c.compiler.option.include.paths" valueType="includePath">
{includes_list}
								</option>
								<option id="ckcoregcc.c.compiler.option.other.riscv64.other.20776496" name="Other flags" superClass="ckcoregcc.c.compiler.option.other.riscv64.other" value="{other_flags}" valueType="string"/>
								<option id="ckcoregcc.c.compiler.category.other.riscv64.static.503253397" name="compiler with static libraries(-static)" superClass="ckcoregcc.c.compiler.category.other.riscv64.static" value="false" valueType="boolean"/>
								<option id="ckcoregcc.c.compiler.category.other.riscv64.fastmath.721541236" name="Floating point optimization options(-ffast-math)" superClass="ckcoregcc.c.compiler.category.other.riscv64.fastmath" value="false" valueType="boolean"/>
								<option id="ckcoregcc.c.compiler.category.other.riscv64.nobuiltinprintf.2085555999" name="Don't recognize built-in function of printf(-fno-builtin-printf)" superClass="ckcoregcc.c.compiler.category.other.riscv64.nobuiltinprintf" value="false" valueType="boolean"/>
								<option id="ckcoregcc.c.compiler.category.other.riscv64.nocommon.259886091" name="Forbidden to insert uninitialized global variables into common segment(-fno-common)" superClass="ckcoregcc.c.compiler.category.other.riscv64.nocommon" value="false" valueType="boolean"/>
								<option id="ckcoregcc.c.compiler.option.other.ffunctionsection.206898793" name="Place each function item into its own section(-ffunction-sections)" superClass="ckcoregcc.c.compiler.option.other.ffunctionsection" value="true" valueType="boolean"/>
								<option id="ckcoregcc.c.compiler.option.other.fdatasection.1351316111" name="Place each data item into its own section(-fdata-sections)" superClass="ckcoregcc.c.compiler.option.other.fdatasection" value="true" valueType="boolean"/>
								<inputType id="cds.managedbuild.tool.ckcoregcc.c.compiler.input.1843637386" superClass="cds.managedbuild.tool.ckcoregcc.c.compiler.input"/>
							</tool>
							<tool id="cds.managedbuild.tool.ckcoregcc.binary.base.elf.riscv64.474347993" name="CSky Elf Binary Linker" superClass="cds.managedbuild.tool.ckcoregcc.binary.base.elf.riscv64">
                                <option id="ckcoregcc.cpp.binary.option.flags.21755221" name="Binary Linker Flags" superClass="ckcoregcc.cpp.binary.option.flags" value="-c -bbinary" valueType="string"/>
                            </tool>
							<tool id="cds.managedbuild.tool.ckcoregcc.linker.base.elf.riscv64.1811306097" name="CSky Elf Linker" superClass="cds.managedbuild.tool.ckcoregcc.linker.base.elf.riscv64">
								<option id="ckcoregcc.link.option.riscv32.linkfile.1811608081" name="Link file (-T)" superClass="ckcoregcc.link.option.riscv32.linkfile" value="&quot;{linker_script_path}&quot;" valueType="string"/>
								<option id="ckcoregcc.link.option.riscv32.nostdlib.2114489876" name="No startup or default libs (-nostdlib)" superClass="ckcoregcc.link.option.riscv32.nostdlib" value="false" valueType="boolean"/>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.link.option.riscv32.libs.1023304312" name="Libraries (-l)" superClass="ckcoregcc.link.option.riscv32.libs" valueType="libs">
{libs_list}
								</option>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.link.option.paths.673587577" name="Library search path (-L)" superClass="ckcoregcc.link.option.paths" valueType="libPaths">
{libpath_list}
								</option>
								<option id="ckcoregcc.link.option.riscv64.static.1801172755" name="link with static libraries(-static)" superClass="ckcoregcc.link.option.riscv64.static" value="false" valueType="boolean"/>
								<option id="ckcoregcc.link.category.other.526832119" name="Linker flags" superClass="ckcoregcc.link.category.other" value="{linker_flags_var}" valueType="string"/>
                                <inputType id="cds.managedbuild.tool.ckcoregcc.c.linker.input.416418734" superClass="cds.managedbuild.tool.ckcoregcc.c.linker.input">
									<additionalInput kind="additionalinputdependency" paths="$(USER_OBJS)"/>
									<additionalInput kind="additionalinput" paths="$(LIBS)"/>
								</inputType>
							</tool>
						</toolChain>
					</folderInfo>
				</configuration>
			</storageModule>
			<storageModule moduleId="org.eclipse.cdt.core.externalSettings"/>
			<storageModule moduleId="cdsBuildOutput" name="Debug">
				<buildoutput callgraphfile="false" ckmapfile="false" elfbinaryfile="false" elfdisassemblyfile="false" elfembeddedsource="false" elfinformationfile="false" intelhex="true" mapfile="false" motorolahex="false" objectdisassemblyfile="false" objectembeddedsource="false" objectinformationfile="false" preprocessorfile="false"/>
			</storageModule>
		</cconfiguration>
		<cconfiguration id="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.release.1447871359">
			<storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.release.1447871359" moduleId="org.eclipse.cdt.core.settings" name="Release">
				<macros>
					<stringMacro name="ChipPath" type="VALUE_TEXT" value="{chip_path}"/>
					<stringMacro name="BoardPath" type="VALUE_TEXT" value="{board_path}"/>
					<stringMacro name="SolutionPath" type="VALUE_TEXT" value="{solution_path}"/>
				</macros>
                <externalSettings/>
				<extensions>
					<extension id="com.csky.cds.debug.core.RISCV64_ELF" point="org.eclipse.cdt.core.BinaryParser"/>
					<extension id="org.eclipse.cdt.core.GmakeErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
					<extension id="org.eclipse.cdt.core.CWDLocator" point="org.eclipse.cdt.core.ErrorParser"/>
					<extension id="org.eclipse.cdt.core.GCCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
					<extension id="org.eclipse.cdt.core.GASErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
					<extension id="org.eclipse.cdt.core.GLDErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
				</extensions>
			</storageModule>
			<storageModule moduleId="cdtBuildSystem" version="4.0.0">
				<configuration artifactName="${{ProjName}}" buildArtefactType="org.eclipse.cdt.build.core.buildArtefactType.exeWithoutOs" buildProperties="org.eclipse.cdt.build.core.buildArtefactType=org.eclipse.cdt.build.core.buildArtefactType.exeWithoutOs,org.eclipse.cdt.build.core.buildType=org.eclipse.cdt.build.core.buildType.release" cleanCommand="rm -rf" description="" id="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.release.1447871359" name="Release" parent="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.release" postbuildStep="{postbuildStep_var}">
					<folderInfo id="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.release.1447871359." name="/" resourcePath="">
						<toolChain id="cds.managedbuild.toolchain.ckcoregcc.riscv64.exeWithoutOs.release.887639632" name="RISCV64 Elf ToolChain" superClass="cds.managedbuild.toolchain.ckcoregcc.riscv64.exeWithoutOs.release">
							<targetPlatform archList="all" binaryParser="com.csky.cds.debug.core.RISCV64_ELF" id="cds.managedbuild.target.csky.platform.ckcoregcc.base.riscv64.1787029073" name="Debug Platform" osList="win32,linux,uclinux" superClass="cds.managedbuild.target.csky.platform.ckcoregcc.base.riscv64"/>
							<builder buildPath="${{workspace_loc:/fsafd}}/Release" id="cds.managedbuild.target.ckcoregcc.builder.base.riscv64.910175668" keepEnvironmentInBuildfile="false" managedBuildOn="true" name="Gnu Make Builder" superClass="cds.managedbuild.target.ckcoregcc.builder.base.riscv64"/>
							<tool id="cds.managedbuild.tool.ckcoregcc.default.base.elf.riscv64.263516871" name="All Tools Settings" superClass="cds.managedbuild.tool.ckcoregcc.default.base.elf.riscv64">
								<option id="cds.managedbuild.option.ckcoregcc.default.riscv64.cputype.2143220431" name="CPUType" superClass="cds.managedbuild.option.ckcoregcc.default.riscv64.cputype" value="{cpu_type_str}" valueType="enumerated"/>
							</tool>
							<tool id="cds.managedbuild.tool.ckcoregcc.assembler.base.elf.riscv64.1749169930" name="CSky Elf Assembler" superClass="cds.managedbuild.tool.ckcoregcc.assembler.base.elf.riscv64">
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.assembler.option.def.symbols.432036288" name="Defined symbols (-D)" superClass="ckcoregcc.assembler.option.def.symbols" valueType="definedSymbols">
{defined_symbols_list}
								</option>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.both.asm.option.include.paths.616053355" name="Include paths (-I)" superClass="ckcoregcc.both.asm.option.include.paths" valueType="includePath">
{includes_list}
								</option>
                                <option id="ckcoregcc.both.asm.option.flags.1673065261" name="Assembler Flags" superClass="ckcoregcc.both.asm.option.flags" value="{asm_flags_var}" valueType="string"/>
								<inputType id="cds.managedbuild.tool.ckcoregcc.assembler.input2.1441230489" superClass="cds.managedbuild.tool.ckcoregcc.assembler.input2"/>
								<inputType id="cds.managedbuild.tool.ckcoregcc.assembler.input1.1802765038" superClass="cds.managedbuild.tool.ckcoregcc.assembler.input1"/>
							</tool>
							<tool id="cds.managedbuild.tool.ckcoregcc.cpp.compiler.base.elf.riscv64.1939456875" name="CSky Elf C++ Compiler" superClass="cds.managedbuild.tool.ckcoregcc.cpp.compiler.base.elf.riscv64">
								<option id="ckcoregcc.cpp.compiler.option.optimization.level.57073747" name="Optimization Level" superClass="ckcoregcc.cpp.compiler.option.optimization.level" value="Optimize size (-Os)" valueType="enumerated"/>
								<option id="ckcoregcc.cpp.compiler.option.debugging.level.965993691" name="Debug Level" superClass="ckcoregcc.cpp.compiler.option.debugging.level" value="ckcoregcc.cpp.compiler.debugging.level.none" valueType="enumerated"/>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.cpp.compiler.option.preprocessor.def.626050196" name="Defined symbols (-D)" superClass="ckcoregcc.cpp.compiler.option.preprocessor.def" valueType="definedSymbols">
{defined_symbols_list}
								</option>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.cpp.compiler.option.include.paths.454158486" name="Include paths (-I)" superClass="ckcoregcc.cpp.compiler.option.include.paths" valueType="includePath">
{includes_list}
								</option>
                                <option id="ckcoregcc.cpp.compiler.option.other.riscv64.other.1518412211" name="Other flags" superClass="ckcoregcc.cpp.compiler.option.other.riscv64.other" value="{other_cppflags}" valueType="string"/>
								<inputType id="cds.managedbuild.tool.ckcoregcc.cpp.compiler.input.1298562960" superClass="cds.managedbuild.tool.ckcoregcc.cpp.compiler.input"/>
							</tool>
							<tool id="cds.managedbuild.tool.ckcoregcc.c.compiler.base.elf.riscv64.1288872723" name="CSky Elf C Compiler" superClass="cds.managedbuild.tool.ckcoregcc.c.compiler.base.elf.riscv64">
								<option id="ckcoregcc.c.compiler.option.optimization.level.1232194934" name="Optimization Level" superClass="ckcoregcc.c.compiler.option.optimization.level" value="Optimize size (-Os)" valueType="enumerated"/>
								<option id="ckcoregcc.c.compiler.option.debugging.level.112344893" name="Debug Level" superClass="ckcoregcc.c.compiler.option.debugging.level" value="ckcoregcc.c.compiler.debugging.level.none" valueType="enumerated"/>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.c.compiler.option.preprocessor.def.2032418531" name="Defined symbols (-D)" superClass="ckcoregcc.c.compiler.option.preprocessor.def" valueType="definedSymbols">
{defined_symbols_list}
								</option>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.c.compiler.option.include.paths.1583202245" name="Include paths (-I)" superClass="ckcoregcc.c.compiler.option.include.paths" valueType="includePath">
{includes_list}
								</option>
                                <option id="ckcoregcc.c.compiler.option.other.riscv64.other.2122346576" superClass="ckcoregcc.c.compiler.option.other.riscv64.other" value="{other_flags}" valueType="string"/>
								<inputType id="cds.managedbuild.tool.ckcoregcc.c.compiler.input.578823073" superClass="cds.managedbuild.tool.ckcoregcc.c.compiler.input"/>
							</tool>
							<tool id="cds.managedbuild.tool.ckcoregcc.binary.base.elf.riscv64.300125482" name="CSky Elf Binary Linker" superClass="cds.managedbuild.tool.ckcoregcc.binary.base.elf.riscv64">
                                <option id="ckcoregcc.cpp.binary.option.flags.21755221" name="Binary Linker Flags" superClass="ckcoregcc.cpp.binary.option.flags" value="-c -bbinary" valueType="string"/>
                            </tool>
							<tool id="cds.managedbuild.tool.ckcoregcc.linker.base.elf.riscv64.958810591" name="CSky Elf Linker" superClass="cds.managedbuild.tool.ckcoregcc.linker.base.elf.riscv64">
								<option id="ckcoregcc.link.option.riscv32.linkfile.2107524827" name="Link file (-T)" superClass="ckcoregcc.link.option.riscv32.linkfile" value="&quot;{linker_script_path}&quot;" valueType="string"/>
								<option id="ckcoregcc.link.option.riscv32.nostdlib.2114489876" name="No startup or default libs (-nostdlib)" superClass="ckcoregcc.link.option.riscv32.nostdlib" value="false" valueType="boolean"/>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.link.option.riscv32.libs.1023304312" name="Libraries (-l)" superClass="ckcoregcc.link.option.riscv32.libs" valueType="libs">
{libs_list}
								</option>
								<option IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false" id="ckcoregcc.link.option.paths.673587577" name="Library search path (-L)" superClass="ckcoregcc.link.option.paths" valueType="libPaths">
{libpath_list}
								</option>
                                <option id="ckcoregcc.link.category.other.288176502" name="Linker flags" superClass="ckcoregcc.link.category.other" value="{linker_flags_var}" valueType="string"/>
								<inputType id="cds.managedbuild.tool.ckcoregcc.c.linker.input.1141837487" superClass="cds.managedbuild.tool.ckcoregcc.c.linker.input">
									<additionalInput kind="additionalinputdependency" paths="$(USER_OBJS)"/>
									<additionalInput kind="additionalinput" paths="$(LIBS)"/>
								</inputType>
							</tool>
						</toolChain>
					</folderInfo>
				</configuration>
			</storageModule>
			<storageModule moduleId="org.eclipse.cdt.core.externalSettings"/>
		</cconfiguration>
	</storageModule>
	<storageModule moduleId="cdtBuildSystem" version="4.0.0">
		<project id="fsafd.cds.managedbuild.target.ckcoregcc.riscv64.exeWithoutOs.358546178" name="Application Without OS" projectType="cds.managedbuild.target.ckcoregcc.riscv64.exeWithoutOs"/>
	</storageModule>
	<storageModule moduleId="scannerConfiguration">
		<autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId=""/>
		<scannerConfigBuildInfo instanceId="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.debug.210845159;cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.debug.210845159.;cds.managedbuild.tool.ckcoregcc.c.compiler.base.elf.riscv64.1468555868;cds.managedbuild.tool.ckcoregcc.c.compiler.input.1843637386">
			<autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId="com.csky.cds.managedbuilder.core.CDSGCCWinManagedMakePerProjectProfileC"/>
		</scannerConfigBuildInfo>
		<scannerConfigBuildInfo instanceId="cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.release.1447871359;cds.managedbuild.config.ckcoregcc.riscv64.exeWithoutOs.release.1447871359.;cds.managedbuild.tool.ckcoregcc.c.compiler.base.elf.riscv64.1288872723;cds.managedbuild.tool.ckcoregcc.c.compiler.input.578823073">
			<autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId="com.csky.cds.managedbuilder.core.CDSGCCWinManagedMakePerProjectProfileC"/>
		</scannerConfigBuildInfo>
	</storageModule>
	<storageModule moduleId="org.eclipse.cdt.core.LanguageSettingsProviders"/>
	<storageModule moduleId="DebugLaunch">
		<launch BAutoRun="true" BDebugInRom="false" BEcosSystem="false" BFirstReset="false" BLoadImage="true" BNoGraphic="true" BOutputLog="false" BPreloadScript="false" BSecondReset="false" BStopAt="true" Connect="Normal" DebugResetType="Hard Reset" FirstReset="Hard Reset" LockConnect="false" LockDebugResetType="false" LockFirstReset="false" LockLaunchOption="false" LockLaunchSteps="false" LockSResetCommand="true" LockSecondReset="false" Machine="" RTOSType="None" RegisterGroups="" SResetCommand="0" SecondReset="Soft Reset" SimOtherFlags="" StopAtFunction="main"/>
		<flash BChipErase="false" BEraseRange="false" BEraseSectors="true" BFlashProgramming="true" BFlashResetandRun="false" BFlashRunMode="false" BFlashVerify="true" BNotErase="false" EraseLength="" EraseStart="" FlashConnect="Normal" FlashDriverPath="" FlashTemplateName="" LockDownload="false" LockFlash="false" LockSResetCommand="true" PathPreDownload="" SResetCommand="0"/>
		<debugscript ContinueScriptPath="" HResetScriptPath="" InitScriptPath="" LockScriptSelect="false" PreloadScriptPath="" SResetScriptPath="" StopScriptPath=""/>
		<connection BJtagServer="false" BLocalJtag="true" BSimulator="false" BUseDDC="true" Delayformtcr="10" ICECLK="12000" JtagServerIP="localhost" JtagServerPort="1025" LocalJTAGFlags="" LockDebugConnection="false"/>
	</storageModule>
	<storageModule moduleId="cdsBuildSystem">
		<version id="4.1.1">
			<import value="V5.2.12 B20220906"/>
		</version>
	</storageModule>
	<storageModule moduleId="refreshScope"/>
	<storageModule moduleId="org.eclipse.cdt.make.core.buildtargets"/>
</cproject>
'''

aft_script_template = '''
#!/bin/sh

echo "I am in CDS post build."
OBJCOPY=riscv64-unknown-elf-objcopy
OBJDUMP=riscv64-unknown-elf-objdump
ELF_NAME="${PWD}/$1.elf"
MAP_NAME="${PWD}/yoc.map"
SOLUTION_PATH=$2
BOARD_PATH=$3
CHIP_PATH=$4
# echo $ELF_NAME
# echo $SOLUTION_PATH
# echo $BOARD_PATH
# echo $CHIP_PATH
$OBJCOPY -O binary $ELF_NAME ${SOLUTION_PATH}/yoc.bin
$OBJDUMP -d $ELF_NAME > ${SOLUTION_PATH}/yoc.asm
cp $ELF_NAME ${SOLUTION_PATH}/yoc.elf
cp $MAP_NAME ${SOLUTION_PATH}/yoc.map

export SOLUTION_PATH=$SOLUTION_PATH
export BOARD_PATH=$BOARD_PATH
export CHIP_PATH=$CHIP_PATH
export IS_IN_CDS=1

if [ -f "$BOARD_PATH/script/aft_build.sh" ];then
    cd $SOLUTION_PATH
    sh $BOARD_PATH/script/aft_build.sh
fi
'''