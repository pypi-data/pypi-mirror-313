#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/19 15:34
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .ssh_main import MortalSSHMain


class MortalSSH(MortalSSHMain):
    def __init__(self, config):
        super().__init__(config)

    def connect(self):
        return self._connect()

    def close(self):
        self._close()
