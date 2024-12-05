#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

import ast
import re
from collections import OrderedDict
from typing import Union, Tuple, List

from nocmd import Cmd


class DBus:

    def __init__(
            self,
            *,
            service_name: str,
            path: str = None,
            interface: str = None,
            get_interface: str = None,
            set_interface: str = None,
    ):

        self.service_name = service_name
        self.path = path or f"/{service_name.replace('.', '/')}"
        self.interface = interface or service_name
        self.get_interface = get_interface or "org.freedesktop.DBus.Properties.Get"
        self.set_interface = set_interface or "org.freedesktop.DBus.Properties.Set"
        self.cmd = [
            "dbus-send",
            f"--dest={service_name}",
            self.path,
            self.interface
        ]

    def _insert_option(self, option: str):
        if option not in self.cmd:
            self.cmd.insert(1, option)
            self.cmd.insert(2, "--print-reply=literal")

    def _remove_interface(self):
        self.cmd = list(OrderedDict.fromkeys(self.cmd))
        for index, _cmd in enumerate(self.cmd):
            if ("=" not in _cmd and self.interface in _cmd) or self.get_interface == _cmd:
                self.cmd = self.cmd[:index]
                break

    def _add_args(self, type_: str, args: Union[Tuple, List]):
        for arg in args:
            if type_ == "string":
                self.cmd.append(f'string:"{arg}"')
            else:
                self.cmd.append(f'{type_}:{arg}')

    def _execute_cmd(self, run_func):
        try:
            result = run_func(" ".join(self.cmd)).strip()
        except Exception as e:
            raise RuntimeError(f"命令执行失败: {e}")
        return self.parse_dbus_output(result)

    def _reset_cmd(self):
        self.cmd = ["dbus-send"]

    @property
    def session(self):
        self._insert_option("--session")
        return self

    @property
    def system(self):
        self._insert_option("--system")
        return self

    def method(self, method: str):
        self._remove_interface()
        self.cmd.append(f"{self.interface}.{method}")
        return self

    def string(self, *args: str):
        self._add_args("string", args)
        return self

    def variant(self, value_type: str, value):
        """
        添加 variant 参数。

        参数:
            value_type (str): 参数类型。
            value: 参数值。
        """
        self._add_args(f'variant:{value_type}', [value])
        return self

    def int16(self, *args: int):
        self._add_args("int16", args)
        return self

    def int32(self, *args: int):
        self._add_args("int32", args)
        return self

    def bool(self, *args: bool):
        self._add_args("boolean", tuple([str(arg).lower() for arg in args]))
        return self

    @staticmethod
    def parse_dbus_output(dbus_output: str):
        _dbus_output = dbus_output.replace('\n', '')
        if 'string' in _dbus_output:
            result = re.search(r'string "(.*)"', _dbus_output).group(1)
        elif 'int32' in _dbus_output:
            result = int(re.search(r'int32 (.*)', _dbus_output).group(1))
        elif 'boolean' in _dbus_output:
            result = _dbus_output.split()[-1] == 'true'
        elif 'array' in _dbus_output:
            array_part = _dbus_output.split('array [')[1].split(']')[0].strip()
            array_elements = [element.strip() for element in array_part.split() if element.strip()]
            result = array_elements
        elif "variant" in _dbus_output:
            result = _dbus_output.split("variant ")[1].strip()
        elif 'dict' in _dbus_output:
            dict_part = _dbus_output.split('dict entry<')[1].split('>')[:-1]
            result = {}
            for entry in dict_part:
                key, value = entry.split(':')
                key = key.strip().replace('string', '').strip('"')
                value = value.strip().replace('string', '').strip('"')
                result[key] = ast.literal_eval(value)
        else:
            result = dbus_output
        return result

    def send(self):
        return self._execute_cmd(Cmd.run)

    def sudo_send(self, password=None):
        return self._execute_cmd(lambda cmd: Cmd.sudo_run(cmd, password=password))

    def get_property(self, property_name: str, interface=None):
        self._remove_interface()
        self.cmd.append(self.get_interface)
        self._add_args(
            "string",
            [interface or self.interface, property_name]
        )
        return self

    def set_property(self, property_name: str, interface=None):
        self._remove_interface()
        self.cmd.append(self.set_interface)
        self._add_args(
            "string",
            [interface or self.interface, property_name]
        )
        return self
