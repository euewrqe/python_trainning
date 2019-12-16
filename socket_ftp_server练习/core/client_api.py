#!/usr/bin/env python
#--coding: utf-8--
'''
connect "ip:addr":connect to server
put:client to server
get:server to client
'''
from conf import setting
from core import tools
from core import client_sock
from core import auth
import os,shutil

#总的信息:用户名、家目录、当前目录、地址端口
USER_MESSAGE={"user":None,"home_path":None,"current_path":None,
              "addr":None,"socket":None}
def client_trance(ipaddr=None,username=None,password=None):
    '''总入口'''
    print(ipaddr,username,password)
    connect(["connect",ipaddr],username,password)
    while True:
        cmd=input(">>").strip()
        if cmd == "":
            continue
        elif cmd == "exit":
            exit("ftp正在退出")
        cmd_list=cmd.split(" ")
        ret=menu_into(cmd_list)



def connect(cmd_list,username=None,password=None):
    '''
    connect 192.168.1.1:9000
    :param cmd_list:
    :return:
    '''
    try:
        if USER_MESSAGE["addr"] == cmd_list[1] and cmd_list[1]:
            tools.make_color("该服务器已经登陆，用户为%s"%USER_MESSAGE["user"],output=True)
        elif not cmd_list[1]:
            cmd_list[1]=input("请输入服务器地址[ip:port]:")
        if len(cmd_list) == 2:
            ip,port=cmd_list[1].split(":")
            ret=client_sock.connect((ip,int(port)),username,password)
            print(ret)
            if ret["flag"]:
                USER_MESSAGE["user"] = ret["user"]
                USER_MESSAGE["addr"] = cmd_list[1]
                USER_MESSAGE["socket"] = ret["socket"]
                # 指定家目录
                USER_MESSAGE["home_path"] = os.path.join(setting.ALL_CLIENT_DIR, ret["user"])
                USER_MESSAGE["current_path"] = os.path.join(setting.ALL_CLIENT_DIR, ret["user"])
                #如果没有就创建
                if not os.path.exists(USER_MESSAGE["home_path"]):
                    os.makedirs(USER_MESSAGE["home_path"],exist_ok=True)
                print(USER_MESSAGE)
                os.chdir(USER_MESSAGE["home_path"])

            return ret
        else:
            raise IndexError("list index out of range")

    except IndexError as e:
        tools.make_color('''connect 参数不正确,格式为
            connect <ip:addr>
            ''')
        return {"flag": False}

@auth.into(USER_MESSAGE)
def put(cmd_list):
    '''put qingkong.bmp'''
    print(cmd_list)
    try:
        if len(cmd_list) == 2:
            file_path=os.path.join(USER_MESSAGE["current_path"],cmd_list[1])
            if not os.path.exists(file_path):
                raise FileNotFoundError("没找到该文件:%s"%file_path)
            client_sock.put(USER_MESSAGE["socket"],file_path)

        elif len(cmd_list) == 3:
            file_path = os.path.join(USER_MESSAGE["current_path"], cmd_list[1])
            if not os.path.exists(file_path):
                raise FileNotFoundError("没找到该文件:%s"%file_path)
            client_sock.put(USER_MESSAGE["socket"], file_path,cmd_list[2])
        else:
            raise IndexError("list index out of range")
    except FileNotFoundError as e:
        tools.make_color(e)
        return {"flag":False}
    except IndexError as e:
        tools.make_color('''put 参数不正确,格式为
                    put <srcfile>
                    put <srcfile> [dstfile]
                    ''')
        return {"flag": False}

@auth.into(USER_MESSAGE)
def get(cmd_list):
    '''get qingkong.bmp
    get qingkong.bmp a.txt
    '''
    try:
        if len(cmd_list) == 2:
            file_path = os.path.join(USER_MESSAGE["current_path"],cmd_list[1])
            client_sock.get(USER_MESSAGE["socket"],cmd_list[1], file_path)

        elif len(cmd_list) == 3:
            file_path = file_path=os.path.join(USER_MESSAGE["current_path"],cmd_list[2])
            client_sock.get(USER_MESSAGE["socket"], cmd_list[1], file_path)
        else:
            raise IndexError("list index out of range")
    except IndexError as e:
        tools.make_color('''put 参数不正确,格式为
                            put <srcfile>
                            put <srcfile> [dstfile]
                            ''')
        return {"flag": False}

@auth.into(USER_MESSAGE)
def ls2server(cmd_list):
    '''
    :return:
    '''
    try:
        if len(cmd_list) == 1:
            client_sock.ls(USER_MESSAGE["socket"])
        elif len(cmd_list) == 2:
            client_sock.ls(USER_MESSAGE["socket"],cmd_list[1])
        else:
            raise IndexError("list index out of range")
    except IndexError as e:
        tools.make_color('''ls2server 参数不正确,格式为
                            ls2server
                            ls2server [path]
                            ''')
        return {"flag": False}
    pass

#本地
@auth.into(USER_MESSAGE)
def ls(cmd_list):
    '''查看家目录'''
    import glob
    try:
        if len(cmd_list) == 2:
            list_path=os.path.join(USER_MESSAGE["current_path"],cmd_list[1])
            if os.path.isfile(list_path):
                file_list = glob.glob(list_path)
            elif os.path.exists(list_path):
                file_list=glob.glob1(list_path,"*")
            else:
                raise IsADirectoryError("该目录不存在")
        else:
            file_list = glob.glob1(USER_MESSAGE["current_path"], "*")

        for file in file_list:
            print(file)
    except IsADirectoryError as e:
        tools.make_color(e)


@auth.into(USER_MESSAGE)
def pwd(cmd_list):
    print(USER_MESSAGE["current_path"])

@auth.into(USER_MESSAGE)
def mkdir(cmd_list):
    try:
        if len(cmd_list) == 2:
            os.makedirs(cmd_list[1])
            return {"flag": True}
        else:
            raise IndexError('''mkdir 参数不正确,格式为
                    mkdir <directory>
                    ''')
    except OSError as e:
        tools.make_color("该目录已存在")
    except IndexError as e:
        tools.make_color(e)
    finally:
        return {"flag": False}

@auth.into(USER_MESSAGE)
def rmdir(cmd_list):
    try:
        if len(cmd_list) == 2:
            os.removedirs(cmd_list[1])
            return {"flag": True}
        else:
            raise IndexError('''rmdir 参数不正确,格式为
                    rmdir <directory>
                            ''')
    except OSError as e:
        tools.make_color("该目录不存在")
    except IndexError as e:
        tools.make_color(e)

    finally:
        return {"flag": False}

def rm(cmd_list):
    try:
        if len(cmd_list) == 2:
            path=cmd_list[1]
            os.remove(path)
        else:
            raise IndexError('''rm 参数不正确,格式为
                        rm <file>
                                ''')
    except IndexError as e:
        tools.make_color(e)
        return {"flag": False}


@auth.into(USER_MESSAGE)
def cat(cmd_list):
    if len(cmd_list) == 2:
        with open(cmd_list[1],"rb") as f:
            for line in f:
                print(line.strip())
    else:
        tools.make_color('''cat 参数不正确,格式为
                        cat <file>
                        ''')
        return {"flag": False}

@auth.into(USER_MESSAGE)
def cd(cmd_list):
    if len(cmd_list) == 2:
        try:
            if cmd_list[1].startswith("..") and USER_MESSAGE["home_path"] == \
                            USER_MESSAGE["current_path"]:
                cd_path = USER_MESSAGE["home_path"]
            else:
                cd_path=os.path.join(USER_MESSAGE["current_path"],cmd_list[1])
            cd_path=os.path.abspath(cd_path)
            if os.path.exists(cd_path):
                USER_MESSAGE["current_path"] = cd_path
                os.chdir(USER_MESSAGE["current_path"])
            else:
                raise FileNotFoundError("找不到该目录:%s"%cd_path)
        except FileNotFoundError as e:
            tools.make_color(e)
    else:
        tools.make_color('''cd 参数不正确,格式为
                        cd <file>
                        ''')
        return {"flag": False}



def ftp_help(cmd_list):
    for cmd in cmd_list:
        print(cmd)
    print()
    pass

def menu_into(cmd_list,socket_handle=None):
    '''操作目录'''
    menu_dict={
        "connect":connect,
        "put":put,
        "get":get,
        "ls2server":ls2server,
        #本地目录
        "ls":ls,
        "mkdir":mkdir,
        "rmdir":rmdir,
        "cat":cat,
        "cd":cd,
        "pwd":pwd,

    }
    if cmd_list[0] in menu_dict:
        ret=menu_dict[cmd_list[0]](cmd_list)
        return ret
    elif cmd_list[0] == "help":
        ftp_help(menu_dict.keys())
    else:
        tools.make_color("%s不是命令"%cmd_list[0],output=True)
        return {"flag":False}


