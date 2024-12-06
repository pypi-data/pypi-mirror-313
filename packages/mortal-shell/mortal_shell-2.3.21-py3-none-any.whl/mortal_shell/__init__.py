#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/4/10 15:25
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .shell_main import MortalShellMain


class MortalShell(MortalShellMain):
    def __init__(self, config):
        super().__init__(config)

    def connect(self):
        return self._connect()

    def send(self, command):
        self._send(command)

    def send_command(self, command):
        return self._send_command(command)

    def close(self):
        self._close()
