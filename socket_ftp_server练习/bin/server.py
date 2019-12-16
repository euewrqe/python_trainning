#!/usr/bin/env python
#--coding: utf-8--
import os,sys
# 添加全局目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import server_sock

opera=input("[server/manage]")
if opera == "server":
    server_sock.connect()
elif opera == "manage":
    pass