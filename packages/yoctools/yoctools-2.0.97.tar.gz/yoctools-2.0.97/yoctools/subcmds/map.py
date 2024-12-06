# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

import os
import sys
import re
import xlsxwriter
import operator
from yoctools import *

# Installing XlsxWriter:
# $ pip install XlsxWriter
# Or to a non system dir:
# $ pip install --user XlsxWriter

#compiler name
compiler_name = ''
#data compress
data_compress = ''

#excel formats
format_dict_title   = {'bold': True, 'border': 7, 'align': 'left', 'bg_color': '#f55066'}
format_dict_entry_A = {'border': 7, 'align': 'left', 'bg_color': '#dcff93'}
format_dict_entry_B = {'border': 7, 'align': 'left', 'bg_color': '#b8f1cc'}
format_dict_entry_C = {'border': 7, 'align': 'left', 'bg_color': '#b8f1ed'}
format_dict_entry_D = {'border': 7, 'align': 'left', 'bg_color': '#e7dac9'}
format_dict_entry_E = {'border': 7, 'align': 'left', 'bg_color': '#ffe543'}

format_dict_entry_Z = {'border': 7, 'align': 'left', 'bg_color': '#e1622f'}

#toolchain libraries
libname_tch = ['libstdc++.a', 'libm.a', 'libgcc.a', 'libc.a', 'libnosys.a' ]

#library (*.a) parse
def find_lib_owner(libname):
    if libname in libname_tch:
        return 'Toolchain', format_dict_entry_B
    else :
        return 'Unknown', format_dict_entry_Z

#get symbol list from gcc map file
def get_sym_list_gcc(sym_all_list, map_file, mem_map_text):
    #1. get 'mem_map_text'
    # find memory map (without discard and debug sections)
    mem_map_list = re.findall(r'Linker script and memory map([\s\S]+?)OUTPUT', mem_map_text)
    mem_map_text = '' if not mem_map_list else mem_map_list[0]
    if not mem_map_text:
        print ('Can\'t parse memory info, memory info get fail!')
        return
    mem_map_text = mem_map_text.replace('\r', '')

    #2. find all object file (*.o) map info
    sym_all_list_a = re.findall(r' [\.\w]*\.(iram1|text|literal|rodata|rodata1|data|bss|eh_frame)(?:\.(\S+)\n? +| +)(0x\w+) +(0x\w+) +.+[/\\](.+\.a)\((.+\.(o|obj))\)\n', mem_map_text)
    sym_all_list_a = map(lambda arg : {'Type':arg[0], 'Sym':arg[1], 'Addr':int(arg[2], 16),
                    'Size':int(arg[3], 16), 'Lib':arg[4], 'File':arg[5]}, sym_all_list_a)

    sym_all_list_o = re.findall(r' [\.\w]*\.(iram1|text|literal|rodata|data|bss|mmu_tbl|eh_frame)(?:\.(\S+)\n? +| +)(0x\w+) +(0x\w+) +.+[/\\](.+\.(o|obj))\n', mem_map_text)
    sym_all_list_o = map(lambda arg : {'Type':arg[0], 'Sym':arg[1], 'Addr':int(arg[2], 16),
                    'Size':int(arg[3], 16), 'Lib':'null', 'File':arg[4]}, sym_all_list_o)

    sym_com_list_a = re.findall(r' (COMMON) +(0x\w+) +(0x\w+) +.+[/\\](.+\.a)\((.+\.(o|obj))\)\n +0x\w+ +(\w+)\n', mem_map_text)
    sym_com_list_a = map(lambda arg : {'Type':arg[0], 'Sym':arg[5], 'Addr':int(arg[1], 16),
                    'Size':int(arg[2], 16), 'Lib':arg[3], 'File':arg[4]}, sym_com_list_a)

    sym_com_list_o = re.findall(r' (COMMON) +(0x\w+) +(0x\w+) +.+[/\\](.+\.(o|obj))\n +0x\w+ +(\w+)\n', mem_map_text)
    sym_com_list_o = map(lambda arg : {'Type':arg[0], 'Sym':arg[4], 'Addr':int(arg[1], 16),
                    'Size':int(arg[2], 16), 'Lib':'null', 'File':arg[3]}, sym_com_list_o)

    sym_all_list.extend(sym_all_list_a)
    sym_all_list.extend(sym_all_list_o)
    sym_all_list.extend(sym_com_list_a)
    sym_all_list.extend(sym_com_list_o)

#get symbol list from gcc map file
def get_sym_list_armcc(sym_all_list, map_file, mem_map_text):
    #1. get 'mem_map_text'
    mem_map_text = mem_map_text.replace('\r', '')

    #2. find all object file (*.o) map info
    sym_all_list_o = re.findall(r'\s+(0x\w+)\s+(0x\w+)\s+(Zero|Data|Code)\s+(RW|RO)\s+\d+\s+(\S+)\s+(.+\.o)\n', mem_map_text)
    sym_all_list_o = map(lambda arg : {'Addr':arg[0], 'Size':int(arg[1], 16), 'Type':arg[2],
                        'Attr':arg[3], 'Sym':arg[4], 'Lib': 'null', 'File':arg[5]}, sym_all_list_o)
    sym_all_list.extend(sym_all_list_o)

    sym_all_list_a = re.findall(r'\s+(0x\w+)\s+(0x\w+)\s+(Zero|Data|Code)\s+(RW|RO)\s+\d+\s+(\S+)\s+(\w+\.ar?)\((.+\.o)\)\n', mem_map_text)
    sym_all_list_a = map(lambda arg : {'Addr':arg[0], 'Size':int(arg[1], 16), 'Type':arg[2],
                        'Attr':arg[3], 'Sym':arg[4], 'Lib': arg[5], 'File':arg[6]}, sym_all_list_a)
    sym_all_list.extend(sym_all_list_a)

    sym_all_list_l = re.findall(r'\s+(0x\w+)\s+(0x\w+)\s+(Zero|Data|Code)\s+(RW|RO)\s+\d+\s+(\S+)\s+(\w+\.l)\((.+\.o)\)\n', mem_map_text)
    sym_all_list_l = map(lambda arg : {'Addr':arg[0], 'Size':int(arg[1], 16), 'Type':arg[2],
                        'Attr':arg[3], 'Sym':arg[4], 'Lib': arg[5], 'File':arg[6]}, sym_all_list_l)
    sym_all_list.extend(sym_all_list_l)

#library (*.a) parse
def parse_library(sym_all_list, benchbook):
    lib_dic_list = []
    id_list = []

    #for each memmap info, classify by mem type
    for obj_dic in sym_all_list:
        id_str = obj_dic['Lib']
        if id_str not in id_list:
            idx = len(lib_dic_list)
            lib_dic_list.append({'Lib':obj_dic['Lib'], 'ROM':0, 'RAM':0, 'Text':0, 'Rodata':0, 'Data':0, 'Bss':0})
            id_list.append(id_str)
        else:
            idx = id_list.index(id_str)

        if compiler_name == 'gcc':
            if obj_dic['Type'] == 'text' or obj_dic['Type'] == 'literal' or obj_dic['Type'] == 'iram1' or obj_dic['Type'] == 'eh_frame':
                lib_dic_list[idx]['Text'] += obj_dic['Size']
            elif obj_dic['Type'] == 'rodata' or obj_dic['Type'] == 'rodata1':
                lib_dic_list[idx]['Rodata'] += obj_dic['Size']
            elif obj_dic['Type'] == 'data':
                lib_dic_list[idx]['Data'] += obj_dic['Size']
            elif obj_dic['Type'] == 'bss' or obj_dic['Type'] == 'COMMON' or obj_dic['Type'] == 'mmu_tbl':
                lib_dic_list[idx]['Bss'] += obj_dic['Size']
        elif compiler_name == 'armcc':
            if obj_dic['Type'] == 'Code':
                lib_dic_list[idx]['Text'] += obj_dic['Size']
            elif obj_dic['Type'] == 'Data' and obj_dic['Attr'] == 'RO':
                lib_dic_list[idx]['Rodata'] += obj_dic['Size']
            elif obj_dic['Type'] == 'Data' and obj_dic['Attr'] == 'RW':
                lib_dic_list[idx]['Data'] += obj_dic['Size']
            elif obj_dic['Type'] == 'Zero':
                lib_dic_list[idx]['Bss'] += obj_dic['Size']

    #sum ROM and RAM for each library file
    for lib_dic in lib_dic_list:
        lib_dic['ROM'] = lib_dic['Text'] + lib_dic['Rodata'] + lib_dic['Data']
        lib_dic['RAM'] = lib_dic['Text'] + lib_dic['Rodata'] + lib_dic['Data'] + lib_dic['Bss']

    if benchbook:
	    title_format = benchbook.add_format(format_dict_title)

	    #2. add obj_dic_list to excel table
	    worksheet = benchbook.add_worksheet('Library')
	    worksheet.set_column('A:B', 20)
	    worksheet.set_column('C:H', 10)
	    worksheet.set_column('I:J', 12)
	    row = 0

	    #set table title
	    worksheet.write_row(row, 0, ['OWNER', 'MODULE', '', 'TEXT', 'RODATA', 'DATA', 'BSS', '','ROM TOTAL', 'RAM TOTAL'], title_format)
	    row += 1

	    #add table entry
	    lib_dic_list = sorted(lib_dic_list, key=operator.itemgetter('Text'), reverse=True)
	    for lib_dic in lib_dic_list:
	        if lib_dic['RAM'] == 0:
	            continue
	        (lib_owner, format_entry) = find_lib_owner(lib_dic['Lib'])
	        entry_format = benchbook.add_format(format_entry)
	        worksheet.write_row(row, 0, [lib_owner, lib_dic['Lib'], '', lib_dic['Text'], lib_dic['Rodata'],
	                            lib_dic['Data'], lib_dic['Bss'], '',lib_dic['ROM'], lib_dic['RAM']], entry_format)
	        row += 1

	    #table ending, summary
	    worksheet.write_row(row, 0, ['TOTAL (bytes)', '', '', '', '', '', '', '', '', ''], title_format)
	    worksheet.write_formula(row, 3, '=SUM(D2:D' + str(row) + ')', title_format)
	    worksheet.write_formula(row, 4, '=SUM(E2:E' + str(row) + ')', title_format)
	    worksheet.write_formula(row, 5, '=SUM(F2:F' + str(row) + ')', title_format)
	    worksheet.write_formula(row, 6, '=SUM(G2:G' + str(row) + ')', title_format)
	    worksheet.write_formula(row, 8, '=SUM(I2:I' + str(row) + ')', title_format)    
	    worksheet.write_formula(row, 9, '=SUM(J2:J' + str(row) + ')', title_format)
    else:
        sum_a = []
        for _ in range(4):
            sum_a.append(0)
        lib_dic_list = sorted(lib_dic_list, key=operator.itemgetter('Text'), reverse=True)
        # print(lib_dic_list)
        formats = '%-24s %-12s %-12s %-12s %-12s\n'
        maptext = formats % ('Name', 'Text', 'Rodata', 'Data', 'Bss')
        for lib_dic in lib_dic_list:
            sum_a[0] += int(lib_dic['Text'])
            sum_a[1] += int(lib_dic['Rodata'])
            sum_a[2] += int(lib_dic['Data'])
            sum_a[3] += int(lib_dic['Bss'])
            maptext += formats % (lib_dic['Lib'], lib_dic['Text'], lib_dic['Rodata'], lib_dic['Data'], lib_dic['Bss'])
        maptext += formats % ('Total', sum_a[0], sum_a[1], sum_a[2], sum_a[3])
        return maptext


#object file (*.o) parse
def parse_object(sym_all_list, benchbook):
    obj_dic_list = []
    id_list = []

    #for each memmap info, classify by mem type
    for obj_dic in sym_all_list:
        id_str = obj_dic['File'] + obj_dic['Lib']
        if id_str not in id_list:
            idx = len(obj_dic_list)
            obj_dic_list.append({'File':obj_dic['File'], 'Lib':obj_dic['Lib'], 'ROM':0, 'RAM':0, 'Text':0, 'Rodata':0, 'Data':0, 'Bss':0})
            id_list.append(id_str)
        else:
            idx = id_list.index(id_str)

        if compiler_name == 'gcc':
            if obj_dic['Type'] == 'text' or obj_dic['Type'] == 'literal' or obj_dic['Type'] == 'iram1' or obj_dic['Type'] == 'eh_frame':
                obj_dic_list[idx]['Text'] += obj_dic['Size']
            elif obj_dic['Type'] == 'rodata' or obj_dic['Type'] == 'rodata1':
                obj_dic_list[idx]['Rodata'] += obj_dic['Size']
            elif obj_dic['Type'] == 'data':
                obj_dic_list[idx]['Data'] += obj_dic['Size']
            elif obj_dic['Type'] == 'bss' or obj_dic['Type'] == 'COMMON' or obj_dic['Type'] == 'mmu_tbl':
                obj_dic_list[idx]['Bss'] += obj_dic['Size']
        elif compiler_name == 'armcc':
            if obj_dic['Type'] == 'Code':
                obj_dic_list[idx]['Text'] += obj_dic['Size']
            elif obj_dic['Type'] == 'Data' and obj_dic['Attr'] == 'RO':
                obj_dic_list[idx]['Rodata'] += obj_dic['Size']
            elif obj_dic['Type'] == 'Data' and obj_dic['Attr'] == 'RW':
                obj_dic_list[idx]['Data'] += obj_dic['Size']
            elif obj_dic['Type'] == 'Zero':
                obj_dic_list[idx]['Bss'] += obj_dic['Size']

    #sum ROM and RAM for each objrary file
    for obj_dic in obj_dic_list:
        obj_dic['ROM'] = obj_dic['Text'] + obj_dic['Rodata'] + obj_dic['Data']
        obj_dic['RAM'] = obj_dic['Text'] + obj_dic['Rodata'] + obj_dic['Data'] + obj_dic['Bss']

    title_format = benchbook.add_format(format_dict_title)

    #2. add obj_dic_list to excel table
    worksheet = benchbook.add_worksheet('Object')
    worksheet.set_column('A:C', 20)
    worksheet.set_column('D:I', 10)
    worksheet.set_column('J:K', 12)
    row = 0

    #set table title
    worksheet.write_row(row, 0, ['OWNER', 'C FILE', 'MODULE', '', 'TEXT', 'RODATA', 'DATA', 'BSS', '', 'ROM TOTAL', 'RAM TOTAL'], title_format)
    row += 1

    #add table entry
    obj_dic_list = sorted(obj_dic_list, key=operator.itemgetter('RAM'), reverse=True)
    for obj_dic in obj_dic_list:
        (lib_owner, format_entry) = find_lib_owner(obj_dic['Lib'])

        entry_format = benchbook.add_format(format_entry)
        worksheet.write_row(row, 0, [lib_owner, obj_dic['File'], obj_dic['Lib'], '', obj_dic['Text'], obj_dic['Rodata'], 
                            obj_dic['Data'], obj_dic['Bss'], '', obj_dic['ROM'], obj_dic['RAM']], entry_format)
        row += 1

    #table ending, summary
    worksheet.write_row(row, 0, ['TOTAL (bytes)', '', '', '', '', '', '', '', '', '', ''], title_format)
    worksheet.write_formula(row, 4, '=SUM(E2:E' + str(row) + ')', title_format)
    worksheet.write_formula(row, 5, '=SUM(F2:F' + str(row) + ')', title_format)
    worksheet.write_formula(row, 6, '=SUM(G2:G' + str(row) + ')', title_format)
    worksheet.write_formula(row, 7, '=SUM(H2:H' + str(row) + ')', title_format)
    worksheet.write_formula(row, 9, '=SUM(J2:J' + str(row) + ')', title_format)
    worksheet.write_formula(row, 10, '=SUM(K2:K' + str(row) + ')', title_format)    
    
#symbol parse
def parse_symbol(sym_all_list, benchbook):
    func_dic_list = []
    rodt_dic_list = []
    data_dic_list = []
    bss_dic_list = []
    id_list = []

    #for each memmap info, classify by mem type, add table entry
    for sym_dic in sym_all_list:
        if compiler_name == 'gcc':
            if sym_dic['Type'] == 'text' or sym_dic['Type'] == 'literal' or sym_dic['Type'] == 'iram1' or sym_dic['Type'] == 'eh_frame':
                func_dic_list.append({'Sym':sym_dic['Sym'], 'File':sym_dic['File'],
                                      'Lib':sym_dic['Lib'], 'Size':sym_dic['Size']})
            elif sym_dic['Type'] == 'rodata':
                rodt_dic_list.append({'Sym':sym_dic['Sym'], 'File':sym_dic['File'],
                                      'Lib':sym_dic['Lib'], 'Size':sym_dic['Size']})
            elif sym_dic['Type'] == 'data':
                data_dic_list.append({'Sym':sym_dic['Sym'], 'File':sym_dic['File'],
                                      'Lib':sym_dic['Lib'], 'Size':sym_dic['Size']})
            elif sym_dic['Type'] == 'bss' or sym_dic['Type'] == 'COMMON':
                bss_dic_list.append({'Sym':sym_dic['Sym'], 'File':sym_dic['File'],
                                      'Lib':sym_dic['Lib'], 'Size':sym_dic['Size']})
        if compiler_name == 'armcc':
            if sym_dic['Type'] == 'Code':
                func_dic_list.append({'Sym':sym_dic['Sym'], 'File':sym_dic['File'],
                                      'Lib':sym_dic['Lib'], 'Size':sym_dic['Size']})
            elif sym_dic['Attr'] == 'RO':
                rodt_dic_list.append({'Sym':sym_dic['Sym'], 'File':sym_dic['File'],
                                      'Lib':sym_dic['Lib'], 'Size':sym_dic['Size']})
            else:
                data_dic_list.append({'Sym':sym_dic['Sym'], 'File':sym_dic['File'],
                                      'Lib':sym_dic['Lib'], 'Size':sym_dic['Size']})

    title_format = benchbook.add_format(format_dict_title)

    #2. add func_dic_list to excel table
    worksheet = benchbook.add_worksheet('Function')
    worksheet.set_column('A:D', 20)
    worksheet.set_column('E:E', 10)
    row = 0

    worksheet.write_row(row, 0, ['OWNER', 'FUNCTION', 'C FILE', 'MODULE', 'SIZE'], title_format)
    row += 1

    func_dic_list = sorted(func_dic_list, key=operator.itemgetter('Size'), reverse=True)
    for sym_dic in func_dic_list:
        (lib_owner, format_entry) = find_lib_owner(sym_dic['Lib'])
        entry_format = benchbook.add_format(format_entry)
        worksheet.write_row(row , 0, [lib_owner, sym_dic['Sym'], sym_dic['File'],
                            sym_dic['Lib'], sym_dic['Size']], entry_format)
        row += 1

    worksheet.write_row(row, 0, ['TOTAL', '', '', ''], title_format)
    worksheet.write_formula(row, 4, '=SUM(E2:E' + str(row) + ')', title_format)

    #3. add func_dic_list to excel table
    worksheet = benchbook.add_worksheet('Rodata')
    worksheet.set_column('A:D', 20)
    worksheet.set_column('E:E', 10)
    row = 0

    worksheet.write_row(row, 0, ['OWNER', 'Rodata', 'C FILE', 'MODULE', 'SIZE'], title_format)
    row += 1

    rodt_dic_list = sorted(rodt_dic_list, key=operator.itemgetter('Size'), reverse=True)
    for sym_dic in rodt_dic_list:
        (lib_owner, format_entry) = find_lib_owner(sym_dic['Lib'])
        entry_format = benchbook.add_format(format_entry)
        worksheet.write_row(row , 0, [lib_owner, sym_dic['Sym'], sym_dic['File'],
                            sym_dic['Lib'], sym_dic['Size']], entry_format)
        row += 1

    worksheet.write_row(row, 0, ['TOTAL', '', '', ''], title_format)
    worksheet.write_formula(row, 4, '=SUM(E2:E' + str(row) + ')', title_format)

    #4. add func_dic_list to excel table
    worksheet = benchbook.add_worksheet('Data')
    worksheet.set_column('A:D', 20)
    worksheet.set_column('E:E', 10)
    row = 0

    worksheet.write_row(row, 0, ['OWNER', 'DATA', 'C FILE', 'MODULE', 'SIZE'], title_format)
    row += 1

    data_dic_list = sorted(data_dic_list, key=operator.itemgetter('Size'), reverse=True)
    for sym_dic in data_dic_list:
        (lib_owner, format_entry) = find_lib_owner(sym_dic['Lib'])
        entry_format = benchbook.add_format(format_entry)
        worksheet.write_row(row , 0, [lib_owner, sym_dic['Sym'], sym_dic['File'],
                            sym_dic['Lib'], sym_dic['Size']], entry_format)
        row += 1

    worksheet.write_row(row, 0, ['TOTAL', '', '', ''], title_format)
    worksheet.write_formula(row, 4, '=SUM(E2:E' + str(row) + ')', title_format)

    #5. add func_dic_list to excel table
    worksheet = benchbook.add_worksheet('Bss')
    worksheet.set_column('A:D', 20)
    worksheet.set_column('E:E', 10)
    row = 0

    worksheet.write_row(row, 0, ['OWNER', 'BSS', 'C FILE', 'MODULE', 'SIZE'], title_format)
    row += 1

    bss_dic_list = sorted(bss_dic_list, key=operator.itemgetter('Size'), reverse=True)
    for sym_dic in bss_dic_list:
        (lib_owner, format_entry) = find_lib_owner(sym_dic['Lib'])
        entry_format = benchbook.add_format(format_entry)
        worksheet.write_row(row , 0, [lib_owner, sym_dic['Sym'], sym_dic['File'],
                            sym_dic['Lib'], sym_dic['Size']], entry_format)
        row += 1

    worksheet.write_row(row, 0, ['TOTAL', '', '', ''], title_format)
    worksheet.write_formula(row, 4, '=SUM(E2:E' + str(row) + ')', title_format)

def get_mem_info(map_file, out_file):
    mem_map_text = ''
    sym_all_list = []
    global compiler_name
    global data_compress

    #1. get 'mem_map_text'
    with open(map_file, 'r') as f:
        mem_map_text = f.read()
        if not mem_map_text:
            print ('Can\'t parse map_file!')
            return
    map_flag = re.findall(r'Memory Map of the image', mem_map_text)
    if not map_flag:
        compiler_name = 'gcc'
        data_compress = 'no'
        get_sym_list_gcc(sym_all_list, map_file, mem_map_text)
    else:
        put_string("Not support yet!")
        return
        compiler_name = 'armcc'
        data_compress = 'yes'
        get_sym_list_armcc(sym_all_list, map_file, mem_map_text)

    if out_file:
        #2. footprint.xlsx parse
        benchbook = xlsxwriter.Workbook(out_file)
        # library (*.a) parse
        parse_library(sym_all_list, benchbook)
        # object file (*.o) parse
        parse_object(sym_all_list, benchbook)
        # symbol parse
        parse_symbol(sym_all_list, benchbook)
        benchbook.close()
    else:
        maptext = parse_library(sym_all_list, None)
        print('----------------------------------------------------------------')
        print(maptext + '----------------------------------------------------------------')


class Map(Command):
    common = True
    helpSummary = "Parse the map file and export as a excel file."
    helpUsage = """
%prog [-f <yoc.map>] [-o <footprint.xlsx>]
"""
    helpDescription = """
Parse the map file and export as a excel file.
"""
    def _Options(self, p):
        p.add_option('-f', '--mapfile',
                     dest='mapfile', action='store', type='str', default=None,
                     help='The map file to parse.')
        p.add_option('-o', '--output',
                     dest='output', action='store', type='str', default=None,
                     help='The output file name. E.g. footprint.xlsx')
    def Execute(self, opt, args):
        yoc = YoC()
        solution = yoc.getSolution(file_non_existent_no_err=True)
        if solution == None:
            put_string("The current directory is not a solution!", level='error')
            exit(0)
        map_file = ''
        if opt.mapfile:
            map_file = opt.mapfile
        else:
            file_list = os.listdir('.')
            for f in file_list:
                if r'.map' in f:
                    map_file = f
                    break
        if os.path.isfile(map_file):
            get_mem_info(map_file, opt.output)
        else:
            put_string("The map file is not found.", level='error')
    
