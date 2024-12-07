#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_requests
=================================================
"""
from typing import Callable

import requests


def request(response_handler: Callable = None, *args, **kwargs):
    """
    call requests.request

    @see https://requests.readthedocs.io/en/latest/
    :param response_handler: response_handler(response)
    :param args: requests.request args
    :param kwargs: requests.request kwargs
    :return: response_handler(response) if isinstance(response_handler, Callable) else response
    """
    response = requests.request(*args, **kwargs)
    if isinstance(response_handler, Callable):
        return response_handler(response)
    return response
