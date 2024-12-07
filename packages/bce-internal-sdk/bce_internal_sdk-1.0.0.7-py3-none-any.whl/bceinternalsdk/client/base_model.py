#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/11/1
# @Author  : zhoubohan
# @File    : base_model.py
"""
from pydantic import BaseModel as BM
from enum import Enum


class BaseModel(BM):
    """
    Base Model contains the common configuration for all pydantic models
    """

    class Config:
        """
        Config contains the common configuration for all pydantic models
        """

        populate_by_name = True
        protected_namespaces = []
        alias_generator = lambda x: x.split("_")[0] + "".join(
            word.capitalize() for word in x.split("_")[1:]
        )

    def json(self, **kwargs):
        """
        Override the json method to convert Enum to its value
        """
        original_dict = super().model_dump(**kwargs)
        for key, value in original_dict.items():
            if isinstance(value, Enum):
                original_dict[key] = value.value
        return super().model_dump_json(by_alias=True, exclude_unset=True, **kwargs)
