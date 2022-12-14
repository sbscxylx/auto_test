#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2022/5/10 18:54
# @Author  : 余少琪
# @Email   : 1603453211@qq.com
# @File    :
# @describe:
"""

import socket
import jenkins


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    _s = None
    try:
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.connect(('8.8.8.8', 80))
        l_host = _s.getsockname()[0]
    finally:
        _s.close()

    return l_host



if __name__ == '__main__':

    # a = ensure_path_sep('/Results/html/index.html')
    # print(a)

    jenkins_server_url = f'http://{get_host_ip()}:8080/jenkins'
    print(jenkins_server_url)