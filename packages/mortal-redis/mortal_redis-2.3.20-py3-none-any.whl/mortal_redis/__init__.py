#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 10:14
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .redis_main import MortalRedisMain


class MortalRedis(MortalRedisMain):
    def __init__(self, config):
        super().__init__(config)

    def close(self):
        self._close()

    def close_db(self, db=0):
        self._close_db(db)

    def set(self, key, value, db=0):
        self._set(key, value, db)

    def get(self, key, db=0):
        return self._get(key, db)

    def set_list(self, key, value: list, db=0):
        self._set_list(key, value, db)

    def get_list(self, key, db=0):
        return self._get_list(key, db)

    def set_dict(self, key, value: dict, db=0):
        self._set_dict(key, value, db)

    def get_dict(self, key, db=0):
        return self._get_dict(key, db)

    def delete(self, key, db=0):
        return self._delete(key, db)

    def get_size(self, db=0):
        return self._get_size(db)

    def pipeline(self, pipe_dict: dict, db=0):
        self._pipeline(pipe_dict, db)

    def keys(self, pattern, db=0):
        return self._keys(pattern, db)
