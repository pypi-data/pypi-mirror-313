#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/16 18:05
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .log_main import MortalLogMain


class MortalLog(MortalLogMain):
    def __init__(self, title=None, file=True, control=True, custom=None, rota=None, time_rota=None):
        super().__init__(title, file, control, custom, rota, time_rota)

    def info(self, *message):
        self._info(*message)

    def debug(self, *message):
        self._debug(*message)

    def warning(self, *message):
        self._warning(*message)

    def error(self, *message):
        self._error(*message)

    def critical(self, *message):
        self._critical(*message)

    def close(self):
        self._close()

    def level(self, level):
        self._set_level(level)

    def file_level(self, level):
        self._set_file_level(level)

    def rota_level(self, level):
        self._set_rota_level(level)

    def time_rota_level(self, level):
        self._set_time_rota_level(level)

    def control_level(self, level):
        self._set_control_level(level)
