#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/16 17:31
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
__all__ = ["MortalFunc"]
from .func_main import MortalFuncMain


class MortalFunc(MortalFuncMain):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
