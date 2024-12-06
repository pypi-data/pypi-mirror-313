# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited

from __future__ import print_function
from yoctools import *

import codecs


class Cdk(Command):
    common = True
    helpSummary = "Generate current solution CDK project"
    helpUsage = """
%prog
"""
    helpDescription = """
generate current solution CDK project.
"""

    def _Options(self, p):
        p.add_option('-d', '--sdk',
                     dest='sdk_name', action='store', type='str', default=None,
                     help='specify chip sdk name, except dummy project.')

    def defines_out(self, defines={}):
        text = ''
        if type(defines) == dict:
            for k, v in defines.items():
                if type(v) == str:
                    text += '{}="{}";'.format(k, v)
                else:
                    text += '{}={};'.format(k, v)
        return text

    def optimize_out(self, ccflags=[]):
        text = '-Os'
        if len(ccflags) > 0:
            for a in ccflags:
                if a.startswith('-O'):
                    text = a  # use last one
        return text
    def hard_float_out(self, linkflags=[]):
        if len(linkflags) > 0:
            if '-mhard-float' in linkflags:
              return 'yes'
        return 'no'

    def Execute(self, opt, args):
        def str_convert(text):
            if sys.version_info.major == 2:
                if type(text) == unicode:
                    text = text.encode('utf8')
            if type(text) != str:
                text = str(text)
            return text

        cpu = platform = kernel = None
        if len(args) > 0:
            cpu = args[0]
        if len(args) > 1:
            platform = args[1]
        if len(args) > 2:
            kernel = args[2]

        def _build_xt_cpu_cdk_proj(cpu, platform, kernel):
            if cpu:
                if not platform:
                    put_string("Please input the platform argument.", level='warning')
                    exit(1)
                put_string("Building [%s/%s/%s] cdk project files, please wait..." % (cpu, platform, kernel))
            elif opt.sdk_name:
                put_string("Building [%s] cdk project files, please wait..." % opt.sdk_name)
            else:
                put_string("Building cdk project files, please wait...")
            put_string(os.getcwd())

            rv_cpu = globals()['RiscvCPU']
            if cpu and (cpu not in rv_cpu):
                put_string("The cpu [%s] is not support yet!" % cpu, level='warning')
                put_string(rv_cpu)
                exit(1)
            platforms = globals()['xt_platforms']
            if platform and (platform not in platforms):
                put_string("The platform [%s] is not support yet!" % platform, level='warning')
                put_string(platforms)
                exit(1)
            kernels = globals()['xt_kernels']
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
                if os.path.isfile(build_chip_yaml_file):
                    shutil.copy2(chip_yaml_file, chip_yaml_file_bak)
                    shutil.copy2(build_chip_yaml_file, chip_yaml_file)
                if os.path.isfile(build_board_yaml_file):
                    shutil.copy2(board_yaml_file, board_yaml_file_bak)
                    shutil.copy2(build_board_yaml_file, board_yaml_file)
                if os.path.isfile(build_sdkchip_yaml_file) and is_have_sdkchip:
                    shutil.copy2(sdkchip_yaml_file, sdkchip_yaml_file_bak)
                    shutil.copy2(build_sdkchip_yaml_file, sdkchip_yaml_file)
                if os.path.isfile(build_solution_yaml_file):
                    shutil.copy2(solution_yaml_file, solution_yaml_file_bak)
                    shutil.copy2(build_solution_yaml_file, solution_yaml_file)

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
                return

            yoc = YoC()
            solution = yoc.getSolution()
            if not solution:
                put_string("The current directory is not a solution!", level='warning')
                _clean_backup_file()
                exit(1)
            if cpu and cpu != solution.cpu_name:
                put_string("The cpu name is not match, please check!", level='warning')
                _clean_backup_file()
                exit(1)
            _clean_backup_file()
            return solution

        yoc = YoC()
        solution = yoc.getSolution()
        if not solution:
            put_string("The current directory is not a solution!", level='warning')
        else:
            packages = ''
            for c in solution.components:
                if c.type != 'solution':
                    packages += '    <Package ID="%s" Version="%s" IsBasic="false"/>\n' % (
                        c.name, c.version)

            if solution.chip_component.name == 'chip_riscv_dummy':
                try:
                    solution = _build_xt_cpu_cdk_proj(cpu, platform, kernel)
                except Exception as ex:
                    put_string(str(ex), level='warning')
                    exit(1)
                packages = ''
                put_string("Build [%s/%s/%s]" % (solution.cpu_name, platform, kernel))

            boardname = 'None'
            boardversion = 'None'
            if solution.board_component:
                boardname = solution.board_component.name
                boardversion = solution.board_component.version

            text = temp.format(name=solution.solution_component.name,
                               description=str_convert(
                                   solution.solution_component.description),
                               chip_name=solution.chip_component.name,
                               chip_version=solution.chip_component.version,
                               board_name=boardname,
                               board_version=boardversion,
                               packages=packages,
                               cpu_name=solution.cpu_name,
                              #  usehardfloat=self.hard_float_out(solution.LINKFLAGS),
                               defines=self.defines_out(solution.defines),
                               optimize=self.optimize_out(solution.CCFLAGS),
                               CCFLAGS=' '.join(solution.CCFLAGS),
                               LINKFLAGS=' '.join(solution.LINKFLAGS),
                               ld_script=solution.ld_script,
                               algorithms_path="$(ProjectPath)/" + os.path.relpath(solution.algorithms_path, os.getcwd()))


            if not os.path.exists(os.path.join(solution.solution_component.path, 'script')):
              try:
                  shutil.copytree(
                      '/usr/local/lib/yoctools/script',
                      os.path.join(solution.solution_component.path, 'script'))
              except Exception as ex:
                  pass
              if solution.board_component:
                  generate_flash_init(os.path.join(solution.board_component.path, 'configs/config.yaml'),
                                      os.path.join(solution.solution_component.path, 'script/flash.init'))

            try:
                filename = os.path.join(solution.solution_component.path,
                                        'project.cdkproj')
                with codecs.open(filename, 'w', 'UTF-8') as f:
                    if sys.version_info.major == 2:
                        if type(text) == str:
                            text = text.decode('UTF-8')
                    f.write(text)
                    put_string("Generate cdk project.cdkproj success.", level='info')
                return True
            except Exception as ex:
                put_string("Generate %s file failed." % filename, level='warning')


temp = '''<?xml version="1.0" encoding="UTF-8"?>
<Project Name="{name}" Version="1">
  <Description>{description}</Description>
  <MonitorProgress>
    <FlashOperate>230</FlashOperate>
    <DebugLaunch>118</DebugLaunch>
  </MonitorProgress>
  <Chips>
    <Chip ID="{chip_name}" Version="{chip_version}" IsBasic="false"/>
  </Chips>
  <Boards>
    <Board ID="{board_name}" Version="{board_version}" IsBasic="false"/>
  </Boards>
  <Packages>
{packages}  </Packages>
  <MergedToYaml>yes</MergedToYaml>
  <DebugSessions>
    <watchExpressions/>
    <memoryExpressions>;;;</memoryExpressions>
    <statistics>;;MHZ;</statistics>
    <peripheralTabs/>
    <WatchDisplayFormat>0</WatchDisplayFormat>
    <LocalDisplayFormat>0</LocalDisplayFormat>
    <debugLayout/>
    <memoryTabColSizeExpressions>100:8;100:8;100:8;100:8;</memoryTabColSizeExpressions>
  </DebugSessions>
  <BuildConfigs>
    <BuildConfig Name="BuildSet">
      <Target>
        <ROMBank Selected="1">
          <ROM1>
            <InUse>yes</InUse>
            <Start>0x20000000</Start>
            <Size>0x1000</Size>
          </ROM1>
          <ROM2>
            <InUse>no</InUse>
            <Start/>
            <Size/>
          </ROM2>
          <ROM3>
            <InUse>no</InUse>
            <Start/>
            <Size/>
          </ROM3>
          <ROM4>
            <InUse>no</InUse>
            <Start/>
            <Size/>
          </ROM4>
          <ROM5>
            <InUse>no</InUse>
            <Start/>
            <Size/>
          </ROM5>
        </ROMBank>
        <RAMBank>
          <RAM1>
            <InUse>no</InUse>
            <Start>0x20001000</Start>
            <Size>0x1000</Size>
            <Init>yes</Init>
          </RAM1>
          <RAM2>
            <InUse>no</InUse>
            <Start/>
            <Size/>
            <Init>yes</Init>
          </RAM2>
          <RAM3>
            <InUse>no</InUse>
            <Start/>
            <Size/>
            <Init>yes</Init>
          </RAM3>
          <RAM4>
            <InUse>no</InUse>
            <Start/>
            <Size/>
            <Init>yes</Init>
          </RAM4>
          <RAM5>
            <InUse>no</InUse>
            <Start/>
            <Size/>
            <Init>yes</Init>
          </RAM5>
        </RAMBank>
        <CPU>{cpu_name}</CPU>
        <UseMiniLib>yes</UseMiniLib>
        <Endian>little</Endian>
        <UseEnhancedLRW>no</UseEnhancedLRW>
        <UseContinueBuild>no</UseContinueBuild>
        <UseSemiHost>no</UseSemiHost>
      </Target>
      <Output>
        <OutputName>$(ProjectName)</OutputName>
        <Type>Executable</Type>
        <CreateHexFile>yes</CreateHexFile>
        <CreateBinFile>no</CreateBinFile>
        <Preprocessor>no</Preprocessor>
        <Disassmeble>yes</Disassmeble>
        <CallGraph>no</CallGraph>
        <Map>yes</Map>
      </Output>
      <User>
        <BeforeCompile>
          <RunUserProg>no</RunUserProg>
          <UserProgName/>
        </BeforeCompile>
        <BeforeMake>
          <RunUserProg>yes</RunUserProg>
          <UserProgName>"$(ProjectPath)/script/before_build.sh"</UserProgName>
        </BeforeMake>
        <AfterMake>
          <RunUserProg>yes</RunUserProg>
          <UserProgName>"$(ProjectPath)/script/after_build.sh"</UserProgName>
        </AfterMake>
      </User>
      <Compiler>
        <Define>{defines}</Define>
        <Undefine/>
        <Optim>Optimize ({optimize})</Optim>
        <DebugLevel>Default (-g)</DebugLevel>
        <IncludePath>$(ProjectPath)/src;$(ProjectPath)/include</IncludePath>
        <OtherFlags>{CCFLAGS}</OtherFlags>
        <Verbose>no</Verbose>
        <Ansi>no</Ansi>
        <Syntax>no</Syntax>
        <Pedantic>no</Pedantic>
        <PedanticErr>no</PedanticErr>
        <InhibitWarn>no</InhibitWarn>
        <AllWarn>yes</AllWarn>
        <WarnErr>no</WarnErr>
        <OneElfS>no</OneElfS>
        <Fstrict>no</Fstrict>
      </Compiler>
      <Asm>
        <Define>{defines}</Define>
        <Undefine/>
        <IncludePath>$(ProjectPath)/src;$(ProjectPath)/include</IncludePath>
        <OtherFlags/>
        <DebugLevel>gdwarf2</DebugLevel>
      </Asm>
      <Linker>
        <Garbage>yes</Garbage>
        <LDFile>$(ProjectPath)/gcc_eflash.ld</LDFile>
        <LibName/>
        <LibPath/>
        <OtherFlags>{LINKFLAGS}</OtherFlags>
        <AutoLDFile>no</AutoLDFile>
        <LinkType/>
      </Linker>
      <Debug>
        <LoadApplicationAtStartup>yes</LoadApplicationAtStartup>
        <Connector>ICE</Connector>
        <StopAt>yes</StopAt>
        <StopAtText>main</StopAtText>
        <InitFile>$(ProjectPath)/script/gdbinit</InitFile>
        <AutoRun>yes</AutoRun>
        <ResetType>Hard Reset</ResetType>
        <SoftResetVal/>
        <ResetAfterLoad>no</ResetAfterLoad>
        <Dumpcore>no</Dumpcore>
        <DumpcoreText>$(ProjectPath)/$(ProjectName).cdkcore</DumpcoreText>
        <ConfigICE>
          <IP>localhost</IP>
          <PORT>1025</PORT>
          <CPUNumber>0</CPUNumber>
          <Clock>12000</Clock>
          <Delay>10</Delay>
          <WaitReset>500</WaitReset>
          <DDC>yes</DDC>
          <TRST>no</TRST>
          <DebugPrint>no</DebugPrint>
          <Connect>Normal</Connect>
          <ResetType>Soft Reset</ResetType>
          <SoftResetVal>0</SoftResetVal>
          <RTOSType>Bare Metal</RTOSType>
          <DownloadToFlash>yes</DownloadToFlash>
          <ResetAfterConnect>no</ResetAfterConnect>
          <GDBName/>
          <GDBServerType>Local</GDBServerType>
          <OtherFlags/>
        </ConfigICE>
        <ConfigSIM>
          <SIMTarget>soccfg/cskyv2/rhea802.xml</SIMTarget>
          <OtherFlags/>
          <NoGraphic>yes</NoGraphic>
          <Log>no</Log>
          <SimTrace>no</SimTrace>
        </ConfigSIM>
      </Debug>
      <Flash>
        <InitFile>$(ProjectPath)/script/flash.init</InitFile>
        <Erase>Erase Sectors</Erase>
        <Algorithms Path="">{algorithms_path}</Algorithms>
        <Program>yes</Program>
        <Verify>yes</Verify>
        <ResetAndRun>no</ResetAndRun>
        <ResetType>Soft Reset</ResetType>
        <SoftResetVal/>
        <External>no</External>
        <Command/>
        <Arguments/>
      </Flash>
    </BuildConfig>
  </BuildConfigs>
  <Dependencies Name="BuildSet"/>
  <PackPathes>$(ProjectPath)/../../components|$(ProjectPath)/../../boards|$(ProjectPath)/Boards|$(ProjectPath)/Chips|$(ProjectPath)/Packages</PackPathes>
</Project>
'''


def generate_flash_init(config_yaml, filename):
    text = '''

{downloads} '''
    v = yaml_load(config_yaml)
    cmd = 'download ihex verify=no $(ProjectPath)/generated/{name}.hex'
    downloads = []
    for k in v['partitions']:
        # put_string(k)
        f = cmd.format(name=k['name'])
        downloads.append(f)

    downloads = '\n'.join(downloads)
    # put_string(s)
    text = text.format(downloads=downloads)
    try:
        with codecs.open(filename, 'w', 'UTF-8') as f:
            f.write(text)
        return True
    except Exception as ex:
        put_string("Generate %s file failed." % filename, level='warning')