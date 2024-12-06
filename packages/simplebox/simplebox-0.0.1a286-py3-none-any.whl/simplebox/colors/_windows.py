#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ctypes
import sys
from enum import Enum

__all__ = []

_handle_map = {sys.stdin: ctypes.windll.kernel32.GetStdHandle(-10),
               sys.stdout: ctypes.windll.kernel32.GetStdHandle(-11),
               sys.stderr: ctypes.windll.kernel32.GetStdHandle(-12)}


class ColorForeground(Enum):
    BLACK = 0x00
    BLUE = 0x01
    GREEN = 0x02
    CYAN = 0x03
    RED = 0x04
    PINK = 0x05
    YELLOW = 0x06
    WHITE = 0x07

    BRIGHT_BLACK = 0x0008 | 0x00
    BRIGHT_RED = 0x0008 | 0x01
    BRIGHT_GREEN = 0x0008 | 0x02
    BRIGHT_YELLOW = 0x0008 | 0x03
    BRIGHT_BLUE = 0x0008 | 0x04
    BRIGHT_PINK = 0x0008 | 0x05
    BRIGHT_CYAN = 0x0008 | 0x06
    BRIGHT_WHITE = 0x0008 | 0x07


class ColorBackground(Enum):
    BLACK = 0x0000
    BLUE = 0x0010
    GREEN = 0x0020
    CYAN = 0x0030
    RED = 0x0040
    PINK = 0x0050
    YELLOW = 0x0060
    WHITE = 0x0070

    BRIGHT_BLACK = 0x0080 | 0x0000
    BRIGHT_RED = 0x0080 | 0x0010
    BRIGHT_GREEN = 0x0080 | 0x0020
    BRIGHT_YELLOW = 0x0080 | 0x0030
    BRIGHT_BLUE = 0x0080 | 0x0040
    BRIGHT_PINK = 0x0080 | 0x0050
    BRIGHT_CYAN = 0x0080 | 0x0060
    BRIGHT_WHITE = 0x0080 | 0x0070


class Style(Enum):
    """
    windows not support
    """
    RESET_ALL = None
    BOLD = None
    WEAKENED = None
    ITALIC = None
    UNDERLINE = None
    SLOW_FLUSH = None
    FAST_FLUSH = None
    REDISPLAY = None


def _color(*objects, sep=' ', end="\n", flush: bool = False, file=sys.stdout,
           cf: ColorForeground = ColorForeground.WHITE,
           cb: ColorBackground = ColorBackground.BLACK, style: Style = None):
    handle = _handle_map.get(file, file)
    cf_attribute = cf.value if cf is not None else ColorForeground.WHITE.value
    cb_attribute = cb.value if cb is not None else ColorBackground.BLACK.value
    attribute = cf_attribute | cb_attribute
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, attribute)
    content = sep.join([str(obj) for obj in objects])
    file.write(content + end)
    if flush is True:
        file.flush()
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, 0x04 | 0x02 | 0x01)


def _dye(string, cf: ColorForeground = ColorForeground.WHITE,
         cb: ColorBackground = ColorBackground.BLACK, style: Style = None):
    raise NotImplementedError("Older Windows cmd.exe not support front dye color, but can output color front.")
