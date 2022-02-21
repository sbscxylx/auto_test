#!/usr/bin/python
# -*- coding: UTF-8 _*_


# 动态调用本地接口还是服务端接口
def server_ip(env):
    """
    dev_ip 开发环境地址
    sit_ip 测试环境服务器地址
    :return:
    """
    if env == "test":
        server_ip = "http://cesces.top"
        return server_ip
    elif env == "realse":
        server_ip = "http://www.coinyee.vip"
        return server_ip
    else:
        print("get envorment ip error")