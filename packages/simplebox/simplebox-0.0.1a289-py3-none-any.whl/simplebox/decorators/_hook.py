#!/usr/bin/env python
# -*- coding:utf-8 -*-

__all__ = []


def _run(meta):
    for hook_, arguments in meta.items():
        args, kwargs = arguments
        hook_(*args, **kwargs)

