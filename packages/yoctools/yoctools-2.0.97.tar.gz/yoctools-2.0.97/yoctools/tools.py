# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
import os
import sys
import time
import hashlib
import zipfile
import codecs
import json
import re
import shutil
import subprocess

try:
    from urlparse import urlparse
    import urllib
    import httplib as http
    urlretrieve = urllib.urlretrieve
    import urllib2 as urllib
except:
    from urllib.parse import urlparse
    import urllib.request
    import http.client as http
    urlretrieve = urllib.request.urlretrieve

from ruamel.yaml import YAML
from ruamel.yaml.constructor import SafeConstructor
from ruamel.yaml.constructor import ConstructorError

class bcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHTGRAY = '\033[37m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def is_contain_chinese(check_str):
    if sys.version_info.major == 2:
        if type(check_str) == str:
            check_str = check_str.decode('utf-8')
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zhPattern.search(check_str)
    if match:
        return True

def is_legal_name(name):
    pattern = re.compile(u'^[_a-zA-Z]\w*$')
    match = pattern.search(name)
    if match:
        return True

def is_legal_depend(depends=[]):
    for d in depends:
        if type(d) == dict:
            v = list(d.values())[0]
            if v.startswith('>='):
                v = v[2:]
                if not v.startswith(' '):
                    put_string("[%s] is illegal.There is no space between '>=' and version" % str(d), level='error')
                    return False
                v = v.lstrip()
                if not (v.startswith('v') or v.startswith('V')):
                    put_string("[%s] is illegal.Version must start with 'v' or 'V'." % str(d), level='error')
                    return False
                v_arr = v[1:].split('.')
                if len(v_arr) < 3:
                    put_string("[%s] is illegal." % str(d), level='error')
                    return False
                else:
                    for a in v_arr:
                        if len(a) > 1 and a.startswith('0'):
                            put_string("[%s] is illegal.Can't start with '0'." % str(d), level='error')
                            return False
                        if a != 'y':
                            try:
                                intvar = int(a)
                                if intvar < 0 or intvar > 99:
                                    put_string("[%s] is illegal.Number must be less than 100." % str(d), level='error')
                                    return False
                            except Exception as e:
                                put_string("[%s], %s" % (str(d), str(e)), level='error')
                                return False
    return True

def latest_ver_get(ver1, ver2):
    if (ver1.startswith('>= v') or ver1.startswith('>= V')) and (ver2.startswith('v') or ver2.startswith('V')):
        num1s = ver1[4:].split('.')
        num2s = ver2[1:].split('.')
        # print(num1s, num2s)
        if len(num1s) == 3 and len(num2s) == 3:
            a1 = int(num1s[0])
            b1 = int(num1s[1])
            c1 = num1s[2]
            if c1 == 'y':
                c1 = 1000
            else:
                c1 = int(c1)
            a2 = int(num2s[0])
            b2 = int(num2s[1])
            c2 = num2s[2]
            if c2 == 'y':
                c2 = 1000
            else:
                c2 = int(c2)
            if a1 < a2:
                return ver2
            elif b1 < b2:
                return ver2
            elif c1 < c2:
                return ver2
            return ver2

# s1 and s2 startwith 'v'
def get_max_version(s1, s2):
        max_version = 'v0.0.0'
        if not s1.startswith('v') or not s2.startswith('v'):
            return max_version
        if s1 == s2:
            max_version = s1
            return max_version
        s1 = s1[1:]
        s2 = s2[1:]
        s1bits = s1.split(".")
        s2bits = s2.split(".")

        if len(s1bits) >= len(s2bits):
            amount = len(s1bits) - len(s2bits)
            for i in range(amount):
                s2bits.append("0")
        else:
            amount = len(s2bits) - len(s1bits)
            for i in range(amount):
                s1bits.append("0")

        for i in range(len(s1bits)):
            try:
                if int(s1bits[i]) > int(s2bits[i]):
                    max_version = s1
                    break
                elif int(s1bits[i]) < int(s2bits[i]):
                    max_version = s2
                    break
                else:
                    max_version = s2
            except IndexError as err:
                pass
        max_version = 'v' + max_version
        return max_version

def del_files_under_dir(path, ignore=[]):
    ls = os.listdir(path)
    for i in ls:
        if i in ignore:
            continue
        f_path = os.path.join(path, i)
        if os.path.isdir(f_path):
            shutil.rmtree(f_path)
        else:
            os.remove(f_path)

def copy_files_under_dir(src_path, dst_path, ignore=[]):
    if os.path.exists(src_path) and os.path.exists(dst_path):
        ls = os.listdir(src_path)
        for i in ls:
            if i in ignore:
                continue
            f_path = os.path.join(src_path, i)
            if os.path.isdir(f_path):
                shutil.copytree(f_path, os.path.join(dst_path, i))
            else:
                shutil.copy2(f_path, dst_path)

def string_len(text):
    L = 0
    R = ''
    if sys.version_info.major == 2:
        if type(text) == str:
            text = text.decode('utf8')
    for c in text:
        if ord(c) >= 0x4E00 and ord(c) <= 0x9FA5:
            L += 2
        else:
            L += 1
    return L

def colors_print(text, color=''):
    if color == 'red':
        print(bcolors.RED + text + bcolors.ENDC, end=' ')
    elif color == 'green':
        print(bcolors.GREEN + text + bcolors.ENDC, end=' ')
    elif color == 'orange':
        print(bcolors.ORANGE + text + bcolors.ENDC, end=' ')
    elif color == 'blue':
        print(bcolors.BLUE + text + bcolors.ENDC, end=' ')
    elif color == 'magenta':
        print(bcolors.MAGENTA + text + bcolors.ENDC, end=' ')
    elif color == 'cyan':
        print(bcolors.CYAN + text + bcolors.ENDC, end=' ')
    elif color == 'lightgray':
        print(bcolors.LIGHTGRAY + text + bcolors.ENDC, end=' ')
    else:
        print(text, end=' ')

def level_print(text, level=''):
    if level == 'info':
        colors_print(text, 'green')
    elif level == 'error':
        colors_print(text, 'red')
    elif level == 'warning':
        colors_print(text, 'orange')
    else:
        colors_print(text)

def put_string(*args, **keys):
    for a in args:
        if sys.version_info.major == 2:
            if type(a) == unicode:
                a = a.encode('utf8')
        if 'key' in keys:
            key = keys['key']
            color_print(a, key=key, end=' ', ignorecase=True)
        elif 'level' in keys:
            level = keys['level']
            level_print(a, level.lower())
        elif 'color' in keys:
            color = keys['color']
            colors_print(a, color.lower())
        else:
            print(a, end=' ')
    print()


def color_print(text, key=[], end='\n', ignorecase=False):
    idx = {}
    itext = text
    if ignorecase:
        itext = text.lower()
    for k in key:
        index = 0
        while True:
            s = itext.find(k, index)
            if s >= 0:
                e = s + len(k)
                need_del = []
                for a, b in idx.items():
                    if max(s, a) <= min(e, b):
                        s = min(s, a)
                        e = max(e, b)
                        need_del.append(a)
                for v in need_del:
                    del idx[v]
                idx[s] = e
                index = e
            else:
                break
    s = 0
    for v in list(sorted(idx)):
        e = v
        print(text[s: e], end='')
        print('\033[1;31m' + text[v: idx[v]] + '\033[0m', end='')
        s = idx[v]
    print(text[s: len(text)], end=end)

duplicatekey = []
def construct_yaml_map(self, node, deep=True):
    global duplicatekey
    keys = set([])
    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=deep)
        if key in keys:
            duplicatekey.append(key)
        keys.add(key)
    return SafeConstructor.construct_mapping(self, node, deep)

def yaml_load(filename):
    global duplicatekey
    try:
        with codecs.open(filename, 'r', encoding='UTF-8') as fh:
            text = fh.read()
            SafeConstructor.add_constructor(u'tag:yaml.org,2002:map', construct_yaml_map)
            ryaml = YAML(typ='safe')
            ryaml.allow_duplicate_keys = True
            data = ryaml.load(text)
            for em in duplicatekey:
                put_string("Found duplicate key: (%s) in file: (%s), please check." % (em, filename), level='warning')
            duplicatekey = []
            return data
    except Exception as e:
        put_string("(%s) in file:%s" % (str(e), filename), level='error')
        exit(-1)


def home_path(path=''):
    return os.path.join(os.path.expanduser('~'), path)


def http2git(url):
    conn = urlparse(url)
    url = 'git@' + conn.netloc + ':' + conn.path[1:]
    return url


def MD5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()


def http_request(method, url, data=None, headers={}):
    conn = urlparse(url)

    if conn.scheme == "https":
        connection = http.HTTPSConnection(conn.netloc)
    else:
        connection = http.HTTPConnection(conn.netloc)
    # connection.debuglevel = 1

    connection.request(method=method, url=conn.path + '?' +
                       conn.query, body=data, headers=headers)
    response = connection.getresponse()
    return response.status, response.read(), response.msg



def http_get(url, path):
    conn = urlparse(url)

    if conn.scheme == "https":
        connection = http.HTTPSConnection(conn.netloc)
    else:
        connection = http.HTTPConnection(conn.netloc)

    connection.request('GET', conn.path)
    response = connection.getresponse()

    filename = os.path.join(path, os.path.basename(conn.path))

    try:
        with codecs.open(filename, 'wb', encoding='UTF-8') as f:
            f.write(response.read())
    except:
        pass

    return filename


def wget(url, out_file):
    start_time = time.time()

    def barProcess(blocknum, blocksize, totalsize):
        speed = (blocknum * blocksize) / (time.time() - start_time)
        # speed_str = " Speed: %.2f" % speed
        speed_str = " Speed: %sB/S         " % format_size(speed)
        recv_size = blocknum * blocksize

        # 设置下载进度条
        f = sys.stdout
        percent = float(recv_size) / totalsize
        if percent > 1:
            percent = 1
        percent_str = " %.2f%%" % (percent * 100)
        n = int(percent * 50)
        s = ('#' * n).ljust(50, '-')
        f.write(percent_str.ljust(9, ' ') + '[' + s + ']' + speed_str)
        f.flush()
        f.write('\r')

    def format_size(bytes):
        bytes = float(bytes)
        kb = bytes / 1024
        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%.3fG" % (G)
            else:
                return "%.3fM" % (M)
        else:
            return "%.3fK" % (kb)

    return urlretrieve(url, out_file, barProcess)


# make_archive(base_name, format, root_dir=None, base_dir=None, verbose=0,dry_run=0, owner=None, group=None, logger=None)
def dfs_get_zip_file(input_path, result):
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '/' + file):
            dfs_get_zip_file(input_path + '/' + file, result)
        else:
            result.append(input_path + '/' + file)


def version_inc(v, x):
    l = len(v)
    num_start = -1
    for i in range(l - 1, -1, -1):
        if num_start == -1:
            if v[i:i + 1].isdigit():
                num_start = i + 1
        else:
            if not v[i:i + 1].isdigit():
                s = v[i + 1:num_start]
                v2 = v.replace(s, str(int(s) + x))
                return v2

    return v + '-0'


def zip_path(input_path, zipName):
    if os.path.isdir(input_path):
        base = os.path.dirname(zipName)
        try:
            os.makedirs(base)
        except:
            pass
        predir = input_path.rsplit('/', 1)[0]
        f = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
        filelists = []
        dfs_get_zip_file(input_path, filelists)
        for file in filelists:
            suffix = os.path.splitext(file)[-1]
            if suffix != '.d' and suffix != '.o':
                f.write(file, file.split(predir)[1])
        f.close()


def write_file(text, filename):
    contents = None

    try:
        with codecs.open(filename, 'r', encoding='UTF-8') as f:
            contents = f.read()
    except:
        pass

    if text == contents:
        return
    try:
        p = os.path.dirname(filename)
        try:
            os.makedirs(p)
        except:
            pass

        with codecs.open(filename, 'w', encoding='UTF-8') as f:
            f.write(text)
    except:
        put_string("Generate %s file failed." % filename, level='error')


def genSConcript(path):
    file_name = os.path.join(path, 'SConscript')
    text = '''Import('defconfig')\ndefconfig.library_yaml()\n'''
    write_file(text, file_name)
    return file_name


def genSConstruct(components, path):
    text = """#! /bin/env python

from yoctools.make import Make

defconfig = Make()

Export('defconfig')

defconfig.build_components()
defconfig.program()
"""

    comp_list = ''
    for component in components:
        if component != '.':
            comp_list += '    "' + component.name + '",\n'

    text = text % comp_list

    script_file = os.path.join(path, 'SConstruct')
    write_file(text, script_file)


def genMakefile(path):
    text = """CPRE := @
ifeq ($(V),1)
CPRE :=
endif


.PHONY:startup
startup: all

all:
	$(CPRE) scons -j4
	@echo YoC SDK Done


.PHONY:clean
clean:
	$(CPRE) rm yoc_sdk -rf
	$(CPRE) scons -c
	$(CPRE) find . -name "*.[od]" -delete

%:
	$(CPRE) scons --component="$@" -j4
"""

    script_file = os.path.join(path, 'Makefile')
    write_file(text, script_file)


def save_yoc_config(defines, filename):
    contents = ""

    try:
        with codecs.open(filename, 'r', encoding='UTF-8') as f:
            contents = f.read()
    except:
        pass

    text = '''/* don't edit, auto generated by tools/toolchain.py */\n
#ifndef __YOC_CONFIG_H__
#define __YOC_CONFIG_H__
#ifndef CONFIG_CPU\n\n'''
    for k, v in defines.items():
        if v in ['y', 'Y']:
            text += '#define %s 1\n' % k
        elif v in ['n', 'N']:
            text += '// #define %s 1\n' % k
        elif type(v) == int:
            text += '#define %s %d\n' % (k, v)
        else:
            text += '#define %s "%s"\n' % (k, v)

    text += '\n#endif\n#endif\n'

    if text == contents:
        return False

    write_file(text, filename)


def save_csi_config(defines, filename):
    text = '''/* don't edit, auto generated by tools/toolchain.py */

#ifndef __CSI_CONFIG_H__
#define __CSI_CONFIG_H__

#include <yoc_config.h>

#endif

'''

    write_file(text, filename)


def check_is_rv_normal_gcc(bin_gcc='gcc'):
    try:
        if bin_gcc.startswith('llvm'):
            return False
        output = subprocess.check_output([bin_gcc, '-v'], stderr=subprocess.STDOUT)
        output = output.decode()
        for line in output.split('\n'):
            if re.search('gcc version', line):
                if re.search('Xuantie', line):
                    return False
    except Exception as ex:
        # print("gcc not found or execute error.", ex)
        return False
    return True
