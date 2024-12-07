#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/8/11 11:40
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : paging.py
# @Software: PyCharm
"""
from typing import List, Optional, Dict, Any


class PagingRequest:
    """
    Represents a paging configuration for retrieving data.

    Args:
        page_no: The page number to retrieve. Default is 0.
        page_size : The number of items per page. Default is 0.
        order : The sorting order for the results. Default is "asc" (ascending).
        orderby : The field by which to order the results. Default is an empty string.
    """

    def __init__(
        self,
        page_no: Optional[int] = 1,
        page_size: Optional[int] = 20,
        order: Optional[str] = "desc",
        orderby: Optional[str] = "",
    ):
        """
        Initializes a new PagingRequest object.
        """
        self.page_no = page_no
        self.page_size = page_size
        self.order = order
        self.orderby = orderby

    def get_page_no(self):
        """
        Get the effective page number to retrieve.

        Returns:
           int: The page number, which defaults to 1 if page_no is 0.
        """
        if self.page_no == 0:
            return 1
        return self.page_no

    def get_page_size(self):
        """
        Get the effective number of items per page.

        Returns:
            int: The number of items per page, which defaults to 20 if page_size is 0.
                   If page_size exceeds 100, it is capped at 100.
        """
        if self.page_size == 0:
            return 20
        if self.page_size > 100:
            return 100
        return self.page_size
