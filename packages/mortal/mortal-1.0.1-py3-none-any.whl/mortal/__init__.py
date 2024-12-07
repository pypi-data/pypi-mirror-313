#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/19 16:51
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .main import MortalMain


class Mortal(MortalMain):
    def __init__(self):
        super().__init__()
