#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/18 10:04
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .ini_main import MortalIniMain


class MortalIni(MortalIniMain):
    def __init__(self, path):
        super().__init__(path)

    def get(self, section, option):
        return self._get(section, option)

    def get_option(self, section):
        return self._get_option(section)

    def get_all(self):
        return self._get_all()

    def set(self, section, option, value, save=True):
        self._set(section, option, value, save)

    def set_option(self, section, option_dict, save=True):
        self._set_option(section, option_dict, save)

    def set_all(self, section_dict, save=True):
        self._set_all(section_dict, save)

    def sections(self):
        return self._sections()

    def options(self, section):
        return self._options(section)

    def remove_section(self, section, save=True):
        self._remove_section(section, save)

    def remove_option(self, section, options, save=True):
        self._remove_option(section, options, save)

    def has_section(self, section):
        return self._has_section(section)

    def has_option(self, section, option):
        return self._has_option(section, option)
