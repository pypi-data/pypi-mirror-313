# cython: language_level=3
# #!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/16 17:08
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .build_main import MortalBuildMain


class MortalBuild(MortalBuildMain):
    def __init__(self, port=None):
        super().__init__(port)

    def build_config(self):
        return self._build_config()

    def build_ext_wheel_pypi(self, config):
        return self._build_ext_wheel_pypi(config)

    def build_ext(self, config):
        self._build_ext(config)

    def build_ext_wheel(self, config):
        return self._build_ext_wheel(config)

    def build_wheel(self, config):
        self._build_wheel(config)
