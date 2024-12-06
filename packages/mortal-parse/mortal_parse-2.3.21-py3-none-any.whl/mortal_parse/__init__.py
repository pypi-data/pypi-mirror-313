#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 13:55
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .sqlparse_main import MortalParseMain


class MortalParse(MortalParseMain):
    def re_hint(self, sql):
        return self._re_hint(sql)

    def parse_sql(self, sql):
        return self._parse_sql(sql)
