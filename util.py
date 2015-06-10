__author__ = 'Marcus'

import distutils.util


def str_to_bool(val):
    return bool(distutils.util.strtobool(val))