# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
import os
import sys
import shutil
import glob

import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

try:
    import SCons.Script as SCons
except:
    import scons
    for path in scons.__path__:
        sys.path.append(path)
        import SCons.Script as SCons

from .log import logger
from .toolchain import *
from .qemu import *


# cpu models defines
CkcoreCPU = ['c807', 'c807f', 'c810', 'c810t', 'c810tv', 'c810v', 'c860', 'c860v', 'ck800', 'ck801', 'ck801t',
             'ck802', 'ck802j', 'ck802t', 'ck803', 'ck803e', 'ck803ef', 'ck803efh', 'ck803efhr1', 'ck803efhr2',
             'ck803efhr3', 'ck803efht', 'ck803efhtr1', 'ck803efhtr2', 'ck803efhtr3', 'ck803efr1', 'ck803efr2',
             'ck803efr3', 'ck803eft', 'ck803eftr1', 'ck803eftr2', 'ck803eftr3', 'ck803eh', 'ck803ehr1', 'ck803ehr2',
             'ck803ehr3', 'ck803eht', 'ck803ehtr1', 'ck803ehtr2', 'ck803ehtr3', 'ck803er1', 'ck803er2', 'ck803er3',
             'ck803et', 'ck803etr1', 'ck803etr2', 'ck803etr3', 'ck803f', 'ck803fh', 'ck803fhr1', 'ck803fhr2', 'ck803fhr3',
             'ck803fr1', 'ck803fr2', 'ck803fr3', 'ck803ft', 'ck803ftr1', 'ck803ftr2', 'ck803ftr3', 'ck803h', 'ck803hr1',
             'ck803hr2', 'ck803hr3', 'ck803ht', 'ck803htr1', 'ck803htr2', 'ck803htr3', 'ck803r1', 'ck803r2', 'ck803r3',
             'ck803s', 'ck803se', 'ck803sef', 'ck803seft', 'ck803sf', 'ck803st', 'ck803t', 'ck803tr1', 'ck803tr2', 'ck803tr3',
             'ck804', 'ck804e', 'ck804ef', 'ck804efh', 'ck804efht', 'ck804eft', 'ck804eh', 'ck804eht', 'ck804et', 'ck804f',
             'ck804fh', 'ck804ft', 'ck804h', 'ck804ht', 'ck804t', 'ck805', 'ck805e', 'ck805ef', 'ck805eft', 'ck805et', 'ck805f',
             'ck805ft', 'ck805t', 'ck807', 'ck807e', 'ck807ef', 'ck807f', 'ck810', 'ck810e', 'ck810ef', 'ck810eft', 'ck810et',
             'ck810f', 'ck810ft', 'ck810ftv', 'ck810fv', 'ck810t', 'ck810tv', 'ck810v', 'ck860', 'ck860f', 'ck860fv', 'ck860v',
             'e801', 'e802', 'e802t', 'e803', 'e803t', 'e804d', 'e804df', 'e804dft', 'e804dt', 'e804f', 'e804ft', 'i805', 'i805f',
             'r807', 'r807f', 's802', 's802t', 's803', 's803t']
RiscvCPU = ['rv32emc', 'rv32ec', 'rv32i', 'rv32iac', 'rv32im', 'rv32imac', 'rv32imafc', 'rv64imac', 'rv64imacxcki', 'rv64imafdc',
            'e902', 'e902m', 'e902t', 'e902mt', 'e906', 'e906f', 'e906fd', 'e906p', 'e906fp', 'e906fdp', 'e907', 'e907f', 'e907fd', 'e907p', 'e907fp', 'e907fdp',
            'c906', 'c906fd', 'c906fdv', 'c908', 'c908v', 'c908i', 'c908-rv32', 'c908v-rv32',
            'c910', 'c910v2', 'c910v3', 'c910v3-cp', 'c920', 'c920v2', 'c920v3', 'c920v3-cp', 'c920v3-ant',
            'r910', 'r920', 'r908', 'r908fd', 'r908fdv', 'r908-cp', 'r908fd-cp', 'r908fdv-cp',
            'c907', 'c907fd', 'c907fdv', 'c907fdvm', 'c907-rv64', 'c907fd-rv64', 'c907fdv-rv64', 'c907fdvm-rv64', 'c907-rv32', 'c907fd-rv32', 'c907fdv-rv32', 'c907fdvm-rv32']
ArmCPU = ['arm1020e', 'arm1020t', 'arm1022e', 'arm1026ej-s', 'arm10e', 'arm10tdmi', 'arm1136j-s', 'arm1136jf-s', 'arm1156t2-s',
            'arm1156t2f-s', 'arm1176jz-s', 'arm1176jzf-s', 'arm2', 'arm250', 'arm3', 'arm6', 'arm60', 'arm600', 'arm610', 'arm620',
            'arm7', 'arm70', 'arm700', 'arm700i', 'arm710', 'arm7100', 'arm710c', 'arm710t', 'arm720', 'arm720t', 'arm740t', 'arm7500',
            'arm7500fe', 'arm7d', 'arm7di', 'arm7dm', 'arm7dmi', 'arm7m', 'arm7tdmi', 'arm7tdmi-s', 'arm8', 'arm810', 'arm9', 'arm920',
            'arm920t', 'arm922t', 'arm926ej-s', 'arm940t', 'arm946e-s', 'arm966e-s', 'arm968e-s', 'arm9e', 'arm9tdmi', 'cortex-a12',
            'cortex-a15', 'cortex-a17', 'cortex-a32', 'cortex-a35', 'cortex-a5','cortex-a53', 'cortex-a57', 'cortex-a7', 'cortex-a72',
            'cortex-a73', 'cortex-a8', 'cortex-a9', 'cortex-m0', 'cortex-m0.small-multiply', 'cortex-m0plus', 'cortex-m0plus.small-multiply',
            'cortex-m1', 'cortex-m1.small-multiply', 'cortex-m23', 'cortex-m3', 'cortex-m33', 'cortex-m33+nodsp', 'cortex-m4', 'cortex-m7',
            'cortex-r4', 'cortex-r4f', 'cortex-r5', 'cortex-r52', 'cortex-r7', 'cortex-r8']

RISCVCPU_MAP = {
    # -mcpu: -march -mabi -mtune
    'e902': ['rv32ec_zicsr_zifencei_xtheadcmo_xtheadse', 'ilp32e', 'e902'],
    'e902m': ['rv32emc_zicsr_zifencei_xtheadcmo_xtheadse', 'ilp32e', 'e902'],
    'e902t': ['rv32ec_zicsr_zifencei_xtheadcmo_xtheadse', 'ilp32e', 'e902'],
    'e902mt': ['rv32emc_zicsr_zifencei_xtheadcmo_xtheadse', 'ilp32e', 'e902'],

    'e906': ['rv32imac_zicntr_zicsr_zifencei_zihpm_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32', 'e906'],
    'e906f': ['rv32imafc_zicntr_zicsr_zifencei_zihpm_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32f', 'e906'],
    'e906fd': ['rv32imafdc_zicntr_zicsr_zifencei_zihpm_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32d', 'e906'],
    'e906p': ['rv32imacp_zicntr_zicsr_zifencei_zihpm_zpn_zpsfoperand_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32', 'e906'],
    'e906fp': ['rv32imafcp_zicntr_zicsr_zifencei_zihpm_zpn_zpsfoperand_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32f', 'e906'],
    'e906fdp': ['rv32imafdcp_zicntr_zicsr_zifencei_zihpm_zpn_zpsfoperand_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32d', 'e906'],

    'e907': ['rv32imac_zicntr_zicsr_zifencei_zihpm_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32', 'e907'],
    'e907f': ['rv32imafc_zicntr_zicsr_zifencei_zihpm_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32f', 'e907'],
    'e907fd': ['rv32imafdc_zicntr_zicsr_zifencei_zihpm_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32d', 'e907'],
    'e907p': ['rv32imacp_zicntr_zicsr_zifencei_zihpm_zpn_zpsfoperand_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32', 'e907'],
    'e907fp': ['rv32imafcp_zicntr_zicsr_zifencei_zihpm_zpn_zpsfoperand_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32f', 'e907'],
    'e907fdp': ['rv32imafdcp_zicntr_zicsr_zifencei_zihpm_zpn_zpsfoperand_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheade_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadsync', 'ilp32d', 'e907'],

    'c906': ['rv64imac_zicntr_zicsr_zifencei_zihpm_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64', 'c906v'],
    'c906fd': ['rv64imafdc_zicntr_zicsr_zifencei_zihpm_zfh_zfhmin_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64d', 'c906v'],
    'c906fdv': ['rv64imafdc_zicntr_zicsr_zifencei_zihpm_zfh_zfhmin_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvector_xtheadzvamo', 'lp64d', 'c906v'],

    'c910': ['rv64imafdc_zicntr_zicsr_zifencei_zihpm_zfh_zfhmin_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64d', 'c910'],
    'c920': ['rv64imafdc_zicntr_zicsr_zifencei_zihpm_zfh_zfhmin_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvector_xtheadzvamo', 'lp64d', 'c910'],
    'r910': ['rv64imafdc_zicntr_zicsr_zifencei_zihpm_zfh_zfhmin_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64d', 'c910'],
    'r920': ['rv64imafdc_zicntr_zicsr_zifencei_zihpm_zfh_zfhmin_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvector_xtheadzvamo', 'lp64d', 'c910'],
    'r908': ['rv64imac_zicbom_zicbop_zicboz_zicntr_zicsr_zifencei_zihintpause_zihpm_zimop_zca_zcb_zcmop_zba_zbb_zbc_zbs_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadfpp_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64', 'c908'],
    'r908fd': ['rv64imafdc_zicbom_zicbop_zicboz_zicntr_zicsr_zifencei_zihintpause_zihpm_zimop_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadfpp_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64d', 'c908'],
    'r908fdv': ['rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicsr_zifencei_zihintpause_zihpm_zimop_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zve32f_zve32x_zve64d_zve64f_zve64x_zvfh_zvl128b_zvl32b_zvl64b_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadfpp_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvdot', 'lp64d', 'c908'],
    'r908-cp': ['rv64imac_zicbom_zicbop_zicboz_zicntr_zicsr_zifencei_zihintpause_zihpm_zimop_zca_zcb_zcmop_zba_zbb_zbc_zbs_sstc_svinval_svnapot_svpbmt_xtheadcmo_xtheadfpp_xtheadsync_xxtccei', 'lp64', 'c908'],
    'r908fd-cp': ['rv64imafdc_zicbom_zicbop_zicboz_zicntr_zicsr_zifencei_zihintpause_zihpm_zimop_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_sstc_svinval_svnapot_svpbmt_xtheadcmo_xtheadfpp_xtheadsync_xxtccef_xxtccei', 'lp64d', 'c908'],
    'r908fdv-cp': ['rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicsr_zifencei_zihintpause_zihpm_zimop_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zve32f_zve32x_zve64d_zve64f_zve64x_zvfh_zvl128b_zvl32b_zvl64b_sstc_svinval_svnapot_svpbmt_xtheadcmo_xtheadfpp_xtheadsync_xxtccef_xxtccei_xxtccev', 'lp64d', 'c908'],

    'c908': ['rv64imafdc_zicbom_zicbop_zicboz_zicntr_zicsr_zifencei_zihintpause_zihpm_zfh_zfhmin_zba_zbb_zbc_zbs_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64d', 'c908'],
    'c908i': ['rv64imac_zicbom_zicbop_zicboz_zicntr_zicsr_zifencei_zihintpause_zihpm_zba_zbb_zbc_zbs_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64', 'c908'],
    'c908v': ['rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicsr_zifencei_zihintpause_zihpm_zfh_zfhmin_zba_zbb_zbc_zbs_zve32f_zve32x_zve64d_zve64f_zve64x_zvfh_zvl128b_zvl32b_zvl64b_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvdot', 'lp64d', 'c908'],
    'c908-rv32': ['rv32imafdc_zicbom_zicbop_zicboz_zicntr_zicsr_zifencei_zihintpause_zihpm_zfh_zfhmin_zba_zbb_zbc_zbs_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'ilp32d', 'c908'],
    'c908v-rv32': ['rv32imafdcv_zicbom_zicbop_zicboz_zicntr_zicsr_zifencei_zihintpause_zihpm_zfh_zfhmin_zba_zbb_zbc_zbs_zve32f_zve32x_zve64d_zve64f_zve64x_zvfh_zvl128b_zvl32b_zvl64b_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvdot', 'ilp32d', 'c908'],

    'c910v2': ['rv64imafdc_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zba_zbb_zbc_zbs_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64d', 'c910'],
    'c910v3': ['rv64imafdc_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64d', 'c910'],
    'c910v3-cp': ['rv64imafdc_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadcmo_xtheadsync_xxtccef_xxtccei', 'lp64d', 'c910'],
    'c920v2': ['rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zba_zbb_zbc_zbs_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvl128b_zvl32b_zvl64b_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvdot', 'lp64d', 'c910'],
    'c920v3': ['rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvl128b_zvl32b_zvl64b_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvdot', 'lp64d', 'c910'],
    'c920v3-cp': ['rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvl128b_zvl32b_zvl64b_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadcmo_xtheadsync_xxtccef_xxtccei_xxtccev', 'lp64d', 'c910'],

    'c907': ['rv64imac_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zawrs_zca_zcb_zba_zbb_zbc_zbs_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64', 'c907'],
    'c907fd': ['rv64imafdc_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zba_zbb_zbc_zbs_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'lp64d', 'c907'],
    'c907fdv': ['rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zba_zbb_zbc_zbs_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvl128b_zvl32b_zvl64b_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvdot', 'lp64d', 'c907'],
    'c907fdvm': ['rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zba_zbb_zbc_zbs_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvl128b_zvl32b_zvl64b_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmatrix_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvdot', 'lp64d', 'c907'],
    'c907-rv32': ['rv32imac_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zawrs_zca_zcb_zba_zbb_zbc_zbs_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'ilp32', 'c907'],
    'c907fd-rv32': ['rv32imafdc_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcf_zba_zbb_zbc_zbs_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync', 'ilp32d', 'c907'],
    'c907fdv-rv32': ['rv32imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcf_zba_zbb_zbc_zbs_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvl128b_zvl32b_zvl64b_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvdot', 'ilp32d', 'c907'],
    'c907fdvm-rv32': ['rv32imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcf_zba_zbb_zbc_zbs_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvl128b_zvl32b_zvl64b_sscofpmf_sstc_svinval_svnapot_svpbmt_xtheadba_xtheadbb_xtheadbs_xtheadc_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadmac_xtheadmatrix_xtheadmemidx_xtheadmempair_xtheadsync_xtheadvdot', 'ilp32d', 'c907'],
}

xt_platforms = ['smartl', 'xiaohui']
xt_kernels = ['rtthread', 'freertos']

class Builder(object):
    def __init__(self, solution, cds_gen=False):
        self.cds_cfgs = {}
        self.cds_gen = cds_gen
        self.toolchain_path = ''
        self.qemu_path = ''
        self.PREFIX = 'csky-abiv2-elf'
        if solution.toolchain_prefix:
            self.PREFIX = solution.toolchain_prefix
        if solution.toolchain_path:
            self.toolchain_path = solution.toolchain_path

        if self.PREFIX == 'llvm':
            self.SIZE = lambda: self.PREFIX + '-size'
            self.OBJDUMP = lambda: self.PREFIX + '-objdump'
            self.OBJCOPY = lambda: self.PREFIX + '-objcopy'
            self.STRIP = lambda: self.PREFIX + '-strip'
            self.AS = lambda: 'clang'
            self.CC = lambda: 'clang'
            self.CXX = lambda: 'clang++'
            self.AR = lambda: self.PREFIX + '-ar'
            self.LINK = lambda: 'clang++'
        else:
            self.SIZE = lambda: self.PREFIX + '-size'
            self.OBJDUMP = lambda: self.PREFIX + '-objdump'
            self.OBJCOPY = lambda: self.PREFIX + '-objcopy'
            self.STRIP = lambda: self.PREFIX + '-strip'
            self.AS = lambda: self.PREFIX + '-gcc'
            self.CC = lambda: self.PREFIX + '-gcc'
            self.CXX = lambda: self.PREFIX + '-g++'
            self.AR = lambda: self.PREFIX + '-ar'
            self.LINK = lambda: self.PREFIX + '-g++'

        self.solution = solution

        self.env = SCons.Environment(tools=['default', 'objcopy', 'objdump', 'product'],
                                     toolpath=[os.path.dirname(
                                         __file__) + '/site_tools'],
                                     AS=self.AS(),
                                     CC=self.CC(),
                                     CXX=self.CXX(),
                                     AR=self.AR(),
                                     LINK=self.CXX(),
                                     OBJCOPY=self.OBJCOPY(),
                                     OBJDUMP=self.OBJDUMP(),
                                     ARFLAGS='-rc',
                                     )

        # self.env.Decider(decide_if_changed)
        self.env.Decider('timestamp-newer')
        # self.env.Decider('make')
        # self.env.Decider('MD5')

        self.env.PrependENVPath('TERM', "xterm-256color")
        # self.env.PrependENVPath('PATH', os.getenv('PATH'))

        if SCons.GetOption('verbose'):
            self.env.Replace(
                ARCOMSTR='AR $TARGET',
                ASCOMSTR='AS $TARGET',
                ASPPCOMSTR='AS $TARGET',
                CCCOMSTR='CC $TARGET',
                CXXCOMSTR='CXX $TARGET',
                LINKCOMSTR = 'LINK $TARGET',
                INSTALLSTR='INSTALL $TARGET',
                BINCOMSTR="Generating $TARGET",
            )

        if self.solution.LINKFLAGS:
            linkflags = self.solution.LINKFLAGS
        else:
            if self.solution.cpu_name.lower().startswith('ck'):
                linkflags = ['-lm', '-Wl,-ckmap="yoc.map"', '-Wl,-zmax-page-size=1024']
            else:
                linkflags = ['-lm', '-Wl,-Map="yoc.map"', '-Wl,-zmax-page-size=1024']
        #fix warning for new toolchain
        #linkflags.append('-Wl,--no-warn-rwx-segments')
        self.set_cpu(self.solution.cpu_name)

        self.env.AppendUnique(
            ASFLAGS=self.solution.ASFLAGS,
            CFLAGS=self.solution.CCFLAGS,
            CXXFLAGS=self.solution.CXXFLAGS,
            LINKFLAGS=linkflags,
        )

        self.env.Replace(AS=self.AS(),
                        CC=self.CC(),
                        CXX=self.CXX(),
                        AR=self.AR(),
                        LINK=self.CXX(),
                        OBJCOPY=self.OBJCOPY(),
                        OBJDUMP=self.OBJDUMP())

        self.cds_cfgs['sources'] = []
        self.cds_cfgs['CPPDEFINES'] = []
        self.cds_cfgs['CPPPATH'] = []
        self.cds_cfgs['CFLAGS'] = []
        self.cds_cfgs['CXXFLAGS'] = []
        self.cds_cfgs['ASFLAGS'] = []
        self.cds_cfgs['LINKFLAGS'] = []

    def set_cpu(self, cpu):
        def set_rv_cpu_flag(flags, cpu_name):
            if not RISCVCPU_MAP[cpu_name]:
                put_string("The cpu [%s] is not support yet!" % cpu_name, level='error')
                exit(1)
            flags.append('-march='+ RISCVCPU_MAP[cpu_name][0])
            flags.append('-mabi=' + RISCVCPU_MAP[cpu_name][1])
            flags.append('-mtune=' + RISCVCPU_MAP[cpu_name][2])
            if cpu_name.startswith('e'):
                flags.append('-mcmodel=medlow')
            else:
                flags.append('-mcmodel=medany')
            return flags

        flags = ['-MP', '-MMD', '-Os', '-Wno-main']
        self.CPU = cpu.lower()
        if self.CPU in CkcoreCPU:
            if not self.PREFIX:
                self.PREFIX = 'csky-abiv2-elf'
            flags.append('-mcpu=' + self.CPU)
            if 'f' in self.CPU:
                flags.append('-mhard-float')
            if self.CPU == 'ck803ef':
                flags.append('-mhigh-registers')
                flags.append('-mdsp')
        elif self.CPU in RiscvCPU:
            if not self.PREFIX:
                self.PREFIX = 'riscv64-unknown-elf'
            elif self.PREFIX.startswith('llvm'):
                pass
            elif not self.PREFIX.startswith('riscv'):
                self.PREFIX = 'riscv64-unknown-elf'

            if self.toolchain_path:
                gccbin = os.path.join(self.toolchain_path, self.PREFIX) + '-gcc'
            else:
                gccbin = self.PREFIX + '-gcc'

            def is_have_arch_options():
                a = b = c = d = False
                for ele in self.solution.CCFLAGS:
                    if ele.startswith("-march="):
                        a = True
                    elif ele.startswith("-mabi="):
                        b = True
                    elif ele.startswith("-mtune="):
                        c = True
                    elif ele.startswith("-mcmodel="):
                        d = True
                    else:
                        pass
                return a, b, c, d
            have_march, have_mabi, have_mtune, have_mcmodel = is_have_arch_options()
            if not have_march:
                is_rv_normal_gcc = check_is_rv_normal_gcc(gccbin)
                if is_rv_normal_gcc:
                    set_rv_cpu_flag(flags, self.CPU)
                else:
                    flags.append('-mcpu=' + self.CPU)
                    if self.CPU.startswith('e'):
                        flags.append('-mcmodel=medlow')
                    else:
                        flags.append('-mcmodel=medany')
            else:
                if not have_mabi:
                    flags.append('-mabi=' + RISCVCPU_MAP[self.CPU][1])
                if not have_mtune:
                    flags.append('-mtune=' + RISCVCPU_MAP[self.CPU][2])
                if not have_mcmodel:
                    if self.CPU.startswith('e'):
                        flags.append('-mcmodel=medlow')
                    else:
                        flags.append('-mcmodel=medany')

        elif self.CPU in ArmCPU:
            if not self.PREFIX:
                self.PREFIX = 'arm-none-eabi'
            #elif not self.PREFIX.startswith('arm'):
            #    self.PREFIX = 'arm-none-eabi'
            flags.append('-mcpu=' + self.CPU)
        else:
            logger.error('error cpu `%s`, please make sure your cpu mode' % self.CPU)
            exit(0)

        self.env.AppendUnique(
            ASFLAGS=flags, CFLAGS=flags,
            CXXFLAGS=flags, LINKFLAGS=flags
        )

    def clone_component(self, component):
        def var_convert(defs):
            if type(defs) == dict:
                vars = {}
                for k, v in defs.items():
                    if type(v) == str:
                        vars[k] = '\\"' + v + '\\"'
                    else:
                        vars[k] = v
                return vars
            else:
                return defs

        env = self.env.Clone()

        if component.build_config.cflag:
            env.AppendUnique(CFLAGS=component.build_config.cflag.split())
        if component.build_config.cxxflag:
            env.AppendUnique(CXXFLAGS=component.build_config.cxxflag.split())
        if component.build_config.asmflag:
            env.AppendUnique(ASFLAGS=component.build_config.asmflag.split())

        env.AppendUnique(CPPPATH=component.build_config.internal_include)
        env.AppendUnique(CPPPATH=self.solution.global_includes)
        env.AppendUnique(CPPDEFINES=var_convert(self.solution.defines))
        env.AppendUnique(CPPDEFINES=var_convert(component.build_config.define))

        # when dummy, use qemu platform
        # if self.solution.variables.get('vendor') == 'dummy':
        #     if self.qemu_path == '':
        #         qemu = QemuYoC()
        #         path = qemu.check_qemu(self.solution.variables.get('arch'))
        #         if path:
        #             self.qemu_path = os.path.dirname(path)
        #     if self.qemu_path:
        #         env.PrependENVPath('PATH', self.qemu_path)
        #     else:
        #         put_string("Not found qemu for %s, please check it." % self.solution.variables.get('arch'), level='error')
        #         exit(-1)

        if self.toolchain_path == '':
            tool = ToolchainYoC()
            path = tool.check_toolchain(self.PREFIX)
            if path:
                self.toolchain_path = os.path.dirname(path)

        if self.toolchain_path and os.path.exists(self.toolchain_path):
            if sys.version_info.major == 2:
                if type(self.toolchain_path) == unicode:
                    self.toolchain_path = self.toolchain_path.encode('utf8')
            if type(self.toolchain_path) != str:
                self.toolchain_path = str(self.toolchain_path)

            env.PrependENVPath('PATH', self.toolchain_path)
        else:
            put_string("Not found toolchain: `%s`, please check it." % os.path.join(self.toolchain_path, self.PREFIX), level='error')
            exit(-1)

        return env

    def build_component(self, component):
        env = self.clone_component(component)

        if self.cds_gen:
            for cf in env['CFLAGS']:
                if cf not in self.cds_cfgs['CFLAGS']:
                    self.cds_cfgs['CFLAGS'].append(cf)

            for cf in env['CXXFLAGS']:
                if cf not in self.cds_cfgs['CXXFLAGS']:
                    self.cds_cfgs['CXXFLAGS'].append(cf)

            for af in env['ASFLAGS']:
                if af not in self.cds_cfgs['ASFLAGS']:
                    self.cds_cfgs['ASFLAGS'].append(af)
            
            for lf in env['LINKFLAGS']:
                if lf not in self.cds_cfgs['LINKFLAGS']:
                    self.cds_cfgs['LINKFLAGS'].append(lf)

            for d in env['CPPDEFINES']:
                if d not in self.cds_cfgs['CPPDEFINES']:
                    self.cds_cfgs['CPPDEFINES'].append(d)

            for fn in env['CPPPATH']:
                if fn not in self.cds_cfgs['CPPPATH']:
                    self.cds_cfgs['CPPPATH'].append(fn)
            # print(cpppath)

            # source files
            sources = []
            for fn in component.source_files:
                fn = os.path.join(os.getcwd(), fn)
                f_list = glob.glob(fn)
                if f_list:
                    for f in f_list:
                        # f = os.path.join(component.name, f)
                        if f not in sources:
                            sources.append(f)
            # print(sources)
            self.cds_cfgs['sources'].extend(sources)
            # print(self.cds_cfgs)
        else:
            sources = []
            for fn in component.source_files:
                f_list = env.Glob(fn)
                if f_list:
                    for f in f_list:
                        if f not in sources:
                            sources.append(f)
            job = env.StaticLibrary(os.path.join(
                self.solution.lib_path, component.name), sources)

        def run_external_script(script_file):
            # print(self.solution.variables.items())
            allv = ''
            for k, v in self.solution.variables.items():
                allv += "%s:%s\\n" % (k, v)
            for comp in self.solution.components:
                allv += "PATH_%s:%s\\n" % (comp.name.upper(), comp.path)
            # print(allv)
            ptext = "-s \"%s\" -b \"%s\" -c \"%s\" -a \"%s\"" % (self.solution.variables.get('SOLUTION_PATH'),
                                                self.solution.variables.get('BOARD_PATH'),
                                                self.solution.variables.get('CHIP_PATH'),
                                                allv)
            if os.path.isfile(script_file):
                os.system('sh %s %s' % (script_file, ptext))
            else:
                logger.warning("The %s is not existed in component %s" % (script_file, component.name))

        def run_postbuild_script(target, source, env):
            for s in component.post_scripts:
                run_external_script(s)

        if component.build_config.prebuild_script:
            if SCons.SCons.SConf.build_type != "clean":
                run_external_script(component.build_config.prebuild_script)

        if not self.cds_gen:
            env.Default(job)

        if component.type == 'solution' and not self.cds_gen:
            # linker script translate
            if self.solution.ld_script.endswith(".S"):
                ld_dst = self.solution.ld_script[:-2]
                ld_path = os.path.join(self.solution.solution_component.path,'out')
                if not os.path.exists(ld_path):
                    try:
                        os.makedirs(ld_path)
                    except:
                        put_string("make dir %s failed." % ld_path, level='error')
                ld_dst = os.path.join(ld_path, os.path.basename(ld_dst))
                # put_string("start to generate linker script from %s to %s" % (self.solution.ld_script, ld_dst))
                cppdefs = ''
                for cppdef in env['CPPDEFINES']:
                    cppdefs += '-D' + cppdef[0] + '=' + str(cppdef[1]) + ' '
                cpppaths = ''
                for cpppath in env['CPPPATH']:
                    cpppaths += '-I' + cpppath + ' '
                cmd = '{cppcmd} -P -C -E {includes} {defines} {ld_src} -o {ld_dst}'.format(
                cppcmd = env['CXX'],
                includes = cpppaths,
                defines = cppdefs,
                ld_src = self.solution.ld_script,
                ld_dst = ld_dst)
                if os.system(cmd) != 0:
                    put_string("failed to generate linker script %s" % ld_dst, level='error')
                    exit(-1)
                self.solution.ld_script = ld_dst
                put_string('success to generate linker script %s' % ld_dst)
            # for libc, it should be -lc, not -llibc
            if component.build_config.linktype == 'start-group':
                linkflags = ' -Wl,--start-group'
            else:
                linkflags = ' -Wl,--whole-archive'
            libs = self.solution.libs
            libs.append(component.name)
            for lib in libs:
                if lib.startswith('lib'):
                    linkflags += ' -l' + lib[3:]
                else:
                    linkflags += ' -l' + lib
            if component.build_config.linktype == 'start-group':
                linkflags += ' -Wl,--end-group'
            else:
                linkflags += ' -Wl,--no-whole-archive'
            linkflags += ' -nostartfiles -Wl,--gc-sections'
            linkflags += ' -T "' + self.solution.ld_script + '"'
            cname = 'yoc'  # component.name
            env.AppendUnique(LINKFLAGS=linkflags.split())
            env.AppendUnique(LIBPATH=self.solution.libpath)
            job = env.Program(target=cname + '.elf', source=[])

            # add recompiled file check.
            env.Depends(job, self.solution.depend_libs)
            env.Depends(job, self.solution.ld_script)
            env.Default(job)

            jobs = []
            dirname = os.path.dirname(env.GetBuildPath("output_xxxd"))
            if env['ELF_FILE']:
                output = os.path.join(dirname, env['ELF_FILE'])
                jj = env.InstallAs(output, job[0])
                jobs.append(jj)

            if env['OBJCOPY_FILE']:
                output = os.path.join(dirname, env['OBJCOPY_FILE'])
                jj = env.Binary(source=job[0], target=output)
                jobs.append(jj)
                if len(component.post_scripts):
                    env.AddPostAction(jj, env.Action(run_postbuild_script))

            if env['OBJDUMP_FILE']:
                output = os.path.join(dirname, env['OBJDUMP_FILE'])
                jj = env.Dump(source=job[0], target=output)
                jobs.append(jj)

            env.Default(jobs)

    def build_image(self, elf=None, objcopy=None, objdump=None, product=None):
        component = self.solution.solution_component
        env = self.clone_component(component)

        source_name = os.path.join('out', component.name, 'yoc.elf')
        if elf and os.path.isfile(source_name):
            shutil.copy2(source_name, elf)


        if objcopy:
            job1 = env.Binary(source=source_name, target=objcopy)
            env.Default(job1)

        if objdump:
            job2 = env.Dump(source=source_name, target=objdump)
            env.Default(job2)
        if product:
            job3 = env.Zip(source='generated/data/config.yaml',
                        target="generated/images.zip", PATH='generated/data')
            job4 = env.Hex(source='generated/images.zip', PATH='generated')
            env.Default(job3)
            env.Default(job4)


def decide_if_changed(dependency, target, prev_ni, repo_node=None):
    # put_string(dependency, prev_ni)
    if not prev_ni:
        return True
    if dependency.get_timestamp() != prev_ni.timestamp:
        return True

    return False
