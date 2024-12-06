#!/usr/bin/env python
# -*- coding:utf-8 -*-

import platform

__py_version = [int(i) for i in platform.python_version().split(".")]
"""
check python version
example:
    python version: 3.9.13
    check_py_version_gt("3.10") => True
    check_py_version_lt("3.10") => False
"""


def check_py_version_gt(version: str):
    for i, v in enumerate(int(i) for i in version.split(".")):
        if __py_version[i] <= v:
            return False
    return True


def check_py_version_ge(version: str):
    for i, v in enumerate(int(i) for i in version.split(".")):
        if v < __py_version[i]:
            return False
    return True


def check_py_version_lt(version: str):
    for i, v in enumerate(int(i) for i in version.split(".")):
        if __py_version[i] >= v:
            return False
    return True


def check_py_version_le(version: str):
    for i, v in enumerate(int(i) for i in version.split(".")):
        if __py_version[i] > v:
            return False
    return True


def check_py_version_eq(version: str):
    for i, v in enumerate(int(i) for i in version.split(".")):
        if __py_version[i] != v:
            return False
    return True


def check_py_version_ne(version: str):
    for i, v in enumerate(int(i) for i in version.split(".")):
        if __py_version[i] == v:
            return False
    return True
