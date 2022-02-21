#!/usr/bin/python
# -*- coding: UTF-8 _*_

import datetime, sys, os, requests, json, base64, ast
from common.Logs import Log

# class return_response(object):
#     def __int__(self, data):
#         self.data = data

file = os.path.basename(sys.argv[0])
log = Log(file)
logger = log.Logger

def dict_style(res):
    try:
        json_response = res.json()
        return True, json_response
    except:
        return False, res

