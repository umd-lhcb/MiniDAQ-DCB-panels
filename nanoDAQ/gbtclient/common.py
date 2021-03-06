#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Jun 29, 2020 at 08:26 PM +0800

from platform import node

from nanoDAQ.utils import hex_rep, dict_factory
from nanoDAQ.exceptions import DIMError, GBTError


#############
# Constants #
#############

GBT_PREF = 'Gbt'
GBT_SERV = node()  # Canonical hostname
TELL40   = 'TELL40_Dev1_0'

# This is defined in 'gbt_sca/inc/constants.h'
SCA_OP_MODE = {
    'write':         0,
    'read':          1,
    'writeread':     2,
    'activate_ch':   3,
    'deactivate_ch': 4,
    'gpio_setdir':   5,
    'gpio_getdir':   6,
    'gpio_setline':  7,
    'gpio_getline':  8,
}


###########
# Helpers #
###########

def fill(s, max_len=128, char='\0'):
    if len(s) > max_len:
        raise ValueError('{} is longer than max length {}.'.format(s, max_len))
    else:
        return s.ljust(max_len, char)


#############################
# Regulate DIM input/output #
#############################

def hex_to_bytes(val):
    if len(val) % 2 == 1:
        val = '0'+val
    return bytes.fromhex(val)


def str_to_hex(val):
    if isinstance(val, int):
        return val
    elif isinstance(val, bytes):
        return hex_rep([int(c) for c in val])
    else:
        return hex_rep([int('{:2x}'.format(ord(c)), base=16) for c in val])


def default_dim_regulator(tp):
    return [str_to_hex(e) for e in tp]


###############################
# Return value error handling #
###############################

def dim_cmd_err(ret_code, expected=1):
    if ret_code != expected:
        raise DIMError('The command was not successfully sent.')


def dim_dic_err(ret, errs, expected=0):
    try:
        ret_code, result = ret[0], ret[1]
    except IndexError:
        ret_code = result = ret[0]

    if ret_code != expected:
        try:
            raise GBTError(errs[ret_code])
        except KeyError:
            raise GBTError('Unknown error with error code {} encountered.'.format(
                hex(ret_code)
            ))

    else:
        return result
