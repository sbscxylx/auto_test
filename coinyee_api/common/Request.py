#!/usr/bin/python
# -*- coding: UTF-8 _*_

import os
import random
import requests
import logging



''' 封装request '''
class RequestsHandler:
    def get_Req(url, params, **kw):  # **kwargs是不定长参数，headers是放在这个不定长参数里
        # '''封装一个get方法，发送get请求'''
        try:  # 当处理不成功时，比如URL地址输入方式错误，或者接口超时timeout，需要抛出一个异常
            res = requests.get(url, params=params, **kw)
            return res
        except TimeoutError:
            # 记录日志信息，放入logger里边，这样我们就能知道问题出在哪里
            logging.error('访问不成功')
            raise


    def post_Req(url, params=None, data=None, json=None, **kw):
        # '''封装一个post方法，发送post请求'''
        try:  # 当处理不成功时，比如URL地址输入方式错误，或者接口超时timeout，需要抛出一个异常
            res = requests.post(url, params=params, data=data, json=json, **kw)  # 其中data是form表单形式的
            return res
        except TimeoutError:
            # 记录日志信息，放入logger里边，这样我们就能知道问题出在哪里
            logging.error('访问不成功')
            raise


    # vist方法是整合接口请求的方法
    def vist_Req(method, url, params=None, data=None, json=None, **kw):
        """访问接口"""
        'GET,如果传输进来的是大写的GET。可以使用lower方法'
        if method.lower() == 'get':
            return RequestsHandler.get_Req(url, params=params, **kw)
        elif method.lower() == 'post':
            return RequestsHandler.post_Req(url, params=params, data=data, json=json, **kw)
        # 如果接口中还有其他的请求方式比如put,option之类色，可以用下方的方法，实际工作中常用的是get和post
        else:
            return requests.request(method, url, **kw)


    # def json_data( method, url, params=None, data=None, json=None, **kw):  # json是要再vist方法下去进行进一步的处理
    #     """访问接口，获取json数据"""
    #     res = RequestsHandler.vist_Req(method, url, params=params, data=data, json=json, **kw)
    #     # 获取json数据
    #     try:
    #         return res.json()
    #     except:
    #         # 记录日志信息
    #         logging.error('不是json格式的数据')
