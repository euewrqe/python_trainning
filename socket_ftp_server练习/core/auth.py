#!/usr/bin/env python
#--coding: utf-8--

from conf import setting
from core import hash_factory,tools
import json,getpass

def login(socket,username=None,password=None):
    '''多用户登陆'''
    while True:
        user_dict={
            "user":input("请输入用户名:") if not username else username,
            "passwd":hash_factory.hash_md5_factory(
                input("请输入密码") if not password else password)
        }
        user_dict=json.dumps(user_dict)
        socket.send_data(user_dict)
        ret_dict=socket.recv_data()
        print(ret_dict)
        ret_dict=json.loads(ret_dict,encoding="utf-8")
        if ret_dict["flag"]:
            tools.make_color(ret_dict["msg"],color="green",output=True)
            return ret_dict
        else:
            tools.make_color(ret_dict["msg"], output=True)
            return ret_dict

def into(user_message):
    #该装饰器用于操作验证
    def auth(func):
        def inner(*args,**kwargs):
            if user_message["user"]:
                ret=func(*args,**kwargs)
                return ret
            else:
                tools.make_color("还没有登陆")
                return {"flag":False}
        return inner
    return auth
