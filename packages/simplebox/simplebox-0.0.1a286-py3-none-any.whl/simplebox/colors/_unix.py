#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from enum import Enum

__all__ = []


class ColorForeground(Enum):
    BLACK = "30"
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    PINK = "35"
    CYAN = "36"
    WHITE = "37"

    BRIGHT_BLACK = "90"
    BRIGHT_RED = "91"
    BRIGHT_GREEN = "92"
    BRIGHT_YELLOW = "93"
    BRIGHT_BLUE = "94"
    BRIGHT_PINK = "95"
    BRIGHT_CYAN = "96"
    BRIGHT_WHITE = "97"


class ColorBackground(Enum):
    BLACK = "40"
    RED = "41"
    GREEN = "42"
    YELLOW = "43"
    BLUE = "44"
    PINK = "45"
    CYAN = "46"
    WHITE = "47"

    BRIGHT_BLACK = "100"
    BRIGHT_RED = "101"
    BRIGHT_GREEN = "102"
    BRIGHT_YELLOW = "103"
    BRIGHT_BLUE = "104"
    BRIGHT_PINK = "105"
    BRIGHT_CYAN = "106"
    BRIGHT_WHITE = "107"


class Style(Enum):
    RESET_ALL = "0"
    BOLD = "1"
    WEAKENED = "2"
    ITALIC = "3"
    UNDERLINE = "4"
    SLOW_FLUSH = "5"
    FAST_FLUSH = "6"
    REDISPLAY = "7"


def _build_template(content, cf: ColorForeground = ColorForeground.WHITE, cb: ColorBackground = None,
                    style: Style = Style.RESET_ALL) -> str:
    if cb is None:
        return "\033[{0};{1}m{2}\033[{3}m".format(style.value, cf.value, content, style.value)
    else:
        return "\033[{0};{1};{2}m{3}\033[{4}m".format(style.value, cf.value, cb.value, content, style.value)


def _color(*objects, sep=' ', end="\n", flush: bool = False, file=sys.stdout,
           cf: ColorForeground = ColorForeground.WHITE,
           cb: ColorBackground = None, style: Style = Style.RESET_ALL):
    file.write(_dye(sep.join([str(obj) for obj in objects]), cf, cb, style) + end)
    if flush is True:
        file.flush()


def _dye(string, cf: ColorForeground = ColorForeground.WHITE,
         cb: ColorBackground = None, style: Style = Style.RESET_ALL):
    content = _build_template(string, cf or ColorForeground.WHITE, cb, style or Style.RESET_ALL)
    return content
