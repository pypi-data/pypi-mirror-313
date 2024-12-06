#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import warnings
import platform
from enum import Enum

"""
unknown platform use print() function
"""

__all__ = []

_PLATFORM_NAME = platform.system()


class ColorForeground(Enum):
    BLACK = None
    RED = None
    GREEN = None
    YELLOW = None
    BLUE = None
    PINK = None
    CYAN = None
    WHITE = None

    BRIGHT_BLACK = None
    BRIGHT_RED = None
    BRIGHT_GREEN = None
    BRIGHT_YELLOW = None
    BRIGHT_BLUE = None
    BRIGHT_PINK = None
    BRIGHT_CYAN = None
    BRIGHT_WHITE = None


class ColorBackground(Enum):
    BLACK = None
    RED = None
    GREEN = None
    YELLOW = None
    BLUE = None
    PINK = None
    CYAN = None
    WHITE = None

    BRIGHT_BLACK = None
    BRIGHT_RED = None
    BRIGHT_GREEN = None
    BRIGHT_YELLOW = None
    BRIGHT_BLUE = None
    BRIGHT_PINK = None
    BRIGHT_CYAN = None
    BRIGHT_WHITE = None


class Style(Enum):
    RESET_ALL = None
    BOLD = None
    WEAKENED = None
    ITALIC = None
    UNDERLINE = None
    SLOW_FLUSH = None
    FAST_FLUSH = None
    REDISPLAY = None


def _color(*objects, sep=' ', end="\n", flush: bool = False, file=sys.stdout,
           cf: ColorForeground = None, cb: ColorBackground = None, style: Style = None):
    file.write(_dye(sep.join([str(obj) for obj in objects]), cf, cb, style) + end)
    if flush is True:
        file.flush()


def _dye(string, cf: ColorForeground = None, cb: ColorBackground = None, style: Style = None):
    warnings.warn(f"color output not support platform: {_PLATFORM_NAME}, use normal string.",
                  category=RuntimeWarning, stacklevel=1, source=None)
    return string
