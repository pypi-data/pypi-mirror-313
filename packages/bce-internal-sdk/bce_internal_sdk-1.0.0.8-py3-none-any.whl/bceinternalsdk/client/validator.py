#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/3/6 10:49
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : validator.py
# @Software: PyCharm
"""
from pydantic import BaseModel
import re

local_name_pattern = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9_-]{0,34}[a-zA-Z0-9])?)?$"
name_regex1 = (r"^workspaces/(?P<workspace_id>.+?)/(?P<parent_type>.+?)s/"
               r"(?P<parent_name>.+?)/(?P<object_type>.+?)s/(.+?)$")
name_regex2 = (
    r"^(?P<parent_type>.+?)s/(?P<parent_name>.+?)/(?P<object_type>.+?)s/(.+?)$"
)

name_regex3 = (
    r"^workspaces/(?P<workspace_id>.+?)/(?P<parent_type>.+?)s/"
    r"(?P<parent_name>.+?)/(?P<object_type>.+?)s/(?P<object_name>.+?)"
    r"/(?P<subobject_type>.+?)s/(?P<subobject_name>.+?)")


class Naming(BaseModel):
    """
    Naming class
    """

    object_type: str
    object_name: str
    parent_type: str = None
    parent_name: str = None
    workspace_id: str = None
    project_name: str = None


def parse_object_name(object_name: str):
    """
    new by object name
    :param object_name:
    :return:
    """
    n = get_name_regex3(object_name)
    if n is None:
        n = get_name_regex1(object_name)
    if n is None:
        n = get_name_regex2(object_name)
    if n is None:
        return None
    else:
        return n


def check(object_name):
    """
    check object name
    :param object_name:
    :return:
    """
    n = get_name_regex3(object_name)
    if n is not None:
        return n
    n = get_name_regex1(object_name)
    if n is not None:
        return n
    n = get_name_regex2(object_name)
    if n is not None:
        return n
    return ValueError("objectName is invalid")


def local_name(local_name: str):
    """
    check local name
    :param local_name:
    :return:
    """
    if re.compile(local_name_pattern).search(local_name) is None:
        return False
    else:
        return True


def get_name_regex1(object_name):
    """
    get name regex1
    :param object_name:
    :return:
    """
    m = re.search(name_regex1, object_name)
    if m is None:
        return None

    num_subexp = len(re.compile(name_regex1).groupindex)
    if len(m.groups()) < num_subexp:
        return None

    n = Naming(
        object_type=m.group("object_type"),
        object_name=object_name,
        parent_name=m.group("parent_name"),
        parent_type=m.group("parent_type"),
        workspace_id=m.group("workspace_id"),
    )

    n.parent_name = ("workspaces/" + n.workspace_id + "/" + n.parent_type +
                     "s/" + m.group("parent_name"))
    return n


def get_name_regex2(object_name):
    """
    get name regex2
    :param object_name:
    :return:
    """
    m = re.search(name_regex2, object_name)
    if m is None:
        return None

    num_subexp = len(re.compile(name_regex2).groupindex)
    if len(m.groups()) < num_subexp:
        return None

    n = Naming(
        object_type=m.group("object_type"),
        object_name=object_name,
        parent_type=m.group("parent_type"),
        parent_name=m.group("parent_name"),
        workspace_id=m.group("parent_name"),
    )

    if n.parent_type == "workspace":
        n.workspace_id = n.parent_name
        n.parent_name = "workspaces/" + n.workspace_id
        return n

    n.parent_name = n.parent_type + "s/" + n.parent_name
    return n


def get_name_regex3(object_name):
    """
    get name regex3
    :param object_name:
    :return:
    """
    m = re.search(name_regex3, object_name)
    if m is None:
        return None

    num_subexp = len(re.compile(name_regex3).groupindex)
    if len(m.groups()) < num_subexp:
        return None

    sub_object_type = m.group("subobject_type")
    if sub_object_type == "" or sub_object_type == "version":
        return None

    n = Naming(
        object_type=m.group("object_type"),
        object_name=object_name,
        parent_type=m.group("parent_type"),
        parent_name=m.group("parent_type") + "s/" + m.group("parent_name") +
        "/" + m.group("object_type") + "s/" + m.group("object_name"),
        workspace_id=m.group("workspace_id"),
    )

    n.parent_name = ("workspaces/" + n.workspace_id + "/" + n.parent_type +
                     "s/" + n.parent_name)

    return n
