#!/usr/bin/env python
#--coding: utf-8--

from core import socket_class
from core import tools
from core import auth,hash_factory
from conf import setting
import os,json

def connect(addr,username=None,password=None):
    try:
        s=socket_class.MySocketClient(addr)
    except ConnectionRefusedError as e:
        tools.make_color("ip:%s,port:%s的连接没有开启"%(addr),output=True)
        return {"flag":False}
    else:
        print(s)
        ret_msg=s.recv_data()
        tools.make_color(ret_msg)
        ret=auth.login(s,username,password)
        ret["socket"]=s

        return ret



def put(s,srcfile,dstfile=None):
    s.send_data("send_file")
    # 迭代获取md5
    srcmd5=hash_factory.file_md5_factory(srcfile)

    #制作文件头部信息
    file_head_dict={"srcfile":srcfile,"dstfile":dstfile,"srcmd5":srcmd5,
               "dstmd5":None}

    file_head=json.dumps(file_head_dict)
    print(file_head)
    s.send_data(file_head)
    s.recv_data()

    #迭代发送,接受进度条

    sfi=s.send_file_iter(file_head_dict["srcfile"])
    for item in sfi:
        part=float(s.recvall_data())
        part=int(part*100)
        tools.view_bar(part, 100)
        pass

    head_dict=s.recvall_data()
    head_dict=json.loads(head_dict)
    if head_dict["srcmd5"] == head_dict["dstmd5"]:
        tools.make_color("文件上传成功",color="green")
        return {"flag":False}
    pass

def get(s,srcfile,dstfile):
    s.send_data("recv_file")
    # 本目标文件制作完，必须得有
    file_head_dict = {"srcfile": srcfile, "dstfile": dstfile, "srcmd5": None,
                      "dstmd5": None}


    print(file_head_dict)
    file_head=json.dumps(file_head_dict)
    s.send_data(file_head)
    file_head_dict=json.loads(s.recv_data())
    print(file_head_dict)
    try:
        if file_head_dict["flag"]:
            tools.make_color(file_head_dict["msg"],color="green")
        else:
            raise FileNotFoundError(file_head_dict["msg"])
    except FileNotFoundError as e:
        tools.make_color(e)
        return {"flag":True}
    else:
        s.send_data("ok")
        rfi=s.recv_file_iter(file_head_dict["dstfile"])
        size,filesize=rfi.__next__()
        print(size,filesize)
        for size in rfi:

            part=size/filesize
            part = int(part * 100)
            tools.view_bar(part, 100)

        dst_md5 = hash_factory.file_md5_factory(file_head_dict["dstfile"])
        file_head_dict["dstmd5"]=dst_md5
        print(file_head_dict)
        if file_head_dict["srcmd5"] == file_head_dict["dstmd5"]:
            tools.make_color("文件上传成功", color="green")
            return {"flag": True}
        pass

def ls(s,path=None):
    '''ls to server'''
    s.send_data("ls")

    if not path:
        s.send_data("?")
    else:
        s.send_data(path)

    dirlist = json.loads(s.recv_data())
    for file in dirlist:
        print(file)
    return {"flag": True}
