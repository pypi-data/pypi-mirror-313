#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 11:03
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .sftp_main import MortalSFTPMain


class MortalSFTP(MortalSFTPMain):
    def __init__(self, config):
        super().__init__(config)

    def connect(self):
        self._connect()

    def remove(self, path):
        return self._remove(path)

    def rename(self, ole_path, new_path):
        return self._rename(ole_path, new_path)

    def posix_rename(self, ole_path, new_path):
        return self._posix_rename(ole_path, new_path)

    def mkdir(self, path):
        return self._mkdir(path)

    def rmdir(self, path):
        return self._rmdir(path)

    def stat(self, file_path):
        return self._stat(file_path)

    def normalize(self, path):
        return self._normalize(path)

    def chdir(self, path):
        return self._chdir(path)

    def upload(self, src_file, dsc_path):
        return self._upload(src_file, dsc_path)

    def download(self, src_file, dsc_path):
        return self._download(src_file, dsc_path)

    def close(self):
        self._close()

