#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import platform
import sys

import psutil

_PLATFORM_NAME = platform.system()


def _get_windows_version():
    if platform.system() != 'Windows':
        return None
    version_info = sys.getwindowsversion()
    if hasattr(version_info, 'platform_version'):
        return tuple(map(int, version_info.platform_version))
    else:
        return version_info.major, version_info.minor, version_info.build


def _is_cmd_exe():
    try:
        parent = psutil.Process(os.getppid())
        return parent.name().lower() == 'cmd.exe'
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


if _PLATFORM_NAME == "Windows":
    windows_version = _get_windows_version()
    if _is_cmd_exe() and windows_version and windows_version < (10, 0, 0):
        from ._windows import ColorForeground, ColorBackground, _dye, _color, Style
    else:
        from ._unix import ColorForeground, ColorBackground, _dye, _color, Style
elif _PLATFORM_NAME in ["Linux", "Darwin"]:
    from ._unix import ColorForeground, ColorBackground, _dye, _color, Style
else:
    from ._unknown import ColorForeground, ColorBackground, _dye, _color, Style

__all__ = []


class Crayon:
    """
    Crayon objects can be used when font colors need to be reused,
    and of course allow colors to be specified temporarily during use without replacing Crayon's colors.

    crayon = Crayon(ColorForeground.RED, style=Style.UNDERLINE)
    crayon("this is RED")
    """

    def __call__(self, *objects, sep=' ', end="\n", flush: bool = False, file=sys.stdout,
                 cf: ColorForeground = None, cb: ColorBackground = None, style: Style = None, **kwargs):
        _color(*objects, sep=sep, end=end, flush=flush, file=file, cf=cf or self.__cf, cb=cb or self.__cb,
               style=style or self.__style)

    def __init__(self, cf: ColorForeground = ColorForeground.WHITE, cb: ColorBackground = None,
                 style: Style = Style.RESET_ALL):
        self.__cf: ColorForeground = cf
        self.__cb: ColorBackground = cb
        self.__style: Style = style

    def dye(self, string, cf: ColorForeground = None, cb: ColorBackground = None, style: Style = None) -> str:
        """
        Output characters that are able to display colors in the console (not supported on older Windows cmd.exe)
        """
        return _dye(string, cf=cf or self.__cf, cb=cb or self.__cb, style=style or self.__style)


def colored(*objects, sep=' ', end="\n", flush: bool = False, file=sys.stdout,
            cf: ColorForeground = ColorForeground.WHITE, cb: ColorBackground = None, style: Style = Style.RESET_ALL):
    """
    A simple terminal color output tool. if you need more advanced color display, you need to implement it yourself.
    :param style: text style
    :param file: a file-like object (stream); defaults to the current sys.stdout.
    :param flush: whether to forcibly flush the stream.
    :param end: string appended after the last value, default a newline.
    :param sep: string inserted between values, default a space.
    :param cf: text color
    :param cb: text background color,default Black
    """
    _color(*objects, sep=sep, end=end, flush=flush, file=file, cf=cf, cb=cb, style=style)


def dye(string, cf: ColorForeground = ColorForeground.WHITE, cb: ColorBackground = None,
        style: Style = Style.RESET_ALL) -> str:
    """
    Output characters that are able to display colors in the console (not supported on older Windows cmd.exe)
    """
    return _dye(string, cf, cb, style)
