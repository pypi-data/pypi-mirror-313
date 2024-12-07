#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/3/21 21:11
# @Author : zhoubohan
# @Email: zhoubohan@baidu.com
# @File : decorator.py
# @Software: PyCharm
"""
import click


def click_options(options):
    """
    This is a decorator that takes a dictionary of options and applies them to a click command.
    :param options:
    :return:
    """

    def decorator(f):
        for name, opts in options.items():
            names = [f"--{name}"]
            if "_" in name:
                names.append(f'--{name.replace("_", "-")}')
            if "-" in name:
                names.append(f'--{name.replace("-", "_")}')
            for option_name in names:
                option = click.option(option_name, **opts)
                f = option(f)
        return f

    return decorator
