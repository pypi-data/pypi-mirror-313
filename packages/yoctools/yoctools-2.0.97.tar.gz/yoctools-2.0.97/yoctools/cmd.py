# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
from .yoc import *
from .subcmds import all_commands
import optparse
import sys
import os

import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

__version__ = "2.0.97"

global_options = optparse.OptionParser(
    usage="yoc COMMAND [ARGS]"
)


class YocCommand:
    def __init__(self):
        self.conf = Configure()
        self.commands = {}
        if self.conf.init:
            self.commands = all_commands
        else:
            self.commands['init'] = all_commands['init']
            self.commands['help'] = all_commands['help']
            self.commands['toolchain'] = all_commands['toolchain']
            all_commands['help'].commands = self.commands

    def _ParseArgs(self, argv):
        """Parse the main `yoc` command line options."""
        name = None
        glob = []

        for i in range(len(argv)):
            if not argv[i].startswith('-'):
                name = argv[i]
                if i > 0:
                    glob = argv[:i]
                argv = argv[i + 1:]
                break
        if not name:
            glob = argv
            name = 'help'
            argv = []
        gopts, _gargs = global_options.parse_args(glob)
        return (name, gopts, argv)

    def _Run(self, name, gopts, argv):
        result = 0
        try:
            cmd = self.commands[name]

        except KeyError:
            if not self.conf.init:
                if name not in all_commands:
                    put_string("`yoc %s` is not a yoc command." %
                        name, file=sys.stderr, level='error')
                else:
                    put_string("`yoc %s` can only be used in the workspace. Please execute `yoc init` to initialize your workspace first. See `yoc help`." %
                            name, file=sys.stderr, level='error')
            else:
                put_string("`yoc %s` is not a yoc command." %
                        name, file=sys.stderr, level='error')
            return 1

        try:
            copts, cargs = cmd.OptionParser.parse_args(argv)
            copts = cmd.ReadEnvironmentOptions(copts)
        except Exception as e:
            put_string('error: in `%s`: %s' % (' '.join([name] + argv), str(e)),
                       file=sys.stderr, level='error')
            put_string('error: manifest missing or unreadable -- please run init',
                       file=sys.stderr, level='error')
            return 1
        try:
            cmd.ValidateOptions(copts, cargs)
            result = cmd.Execute(copts, cargs)
        except Exception as e:
            put_string("YocCommand error:%s" % str(e), level='error')
            pass
        return result

    def Execute(self, argv):
        name, gopts, argv = self._ParseArgs(argv)

        self._Run(name, gopts, argv)


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == '-V' or sys.argv[1] == '--version':
            put_string(__version__)
            return
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            sys.argv[1] = 'help'
    cmd = YocCommand()
    cmd.Execute(sys.argv[1:])

def cct_main():
    try:
        cmd = all_commands['cct']
        parser = cmd.OptionParser
        parser.set_usage(cmd.helpUsage.strip().replace('%prog', cmd.NAME))
        copts, cargs = parser.parse_args(sys.argv[1:])
        copts = cmd.ReadEnvironmentOptions(copts)
    except Exception as e:
        put_string('error: manifest missing or unreadable -- please run init',
                    file=sys.stderr, level='error')
        return 1
    try:
        cmd.ValidateOptions(copts, cargs)
        cmd.Execute(copts, cargs)
    except Exception as e:
        put_string("YocCommand error:%s" % str(e), level='error')
        pass
