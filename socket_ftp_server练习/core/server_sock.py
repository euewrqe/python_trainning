#!/usr/bin/env python
#--coding: utf-8--

from conf import setting
from core.socket_class import MySocketServer
from core import tools,hash_factory
import json,os


def connect():
    class MyServer(MySocketServer):
        def handle(self):
            # 接收用户名和密码
            self.conn = self.request
            self.ip_port = self.client_address
            self.message={
                "pwd":setting.SERVER_DIR
            }


            os.chdir(self.message["pwd"])

            self.send_data("成功连接ftp,请输入用户名和密码")
            # 循环登陆，直到成功
            count = 0
            while True:
                user_dict=self.recv_data()

                user_dict=json.loads(user_dict)
                user_path=os.path.join(setting.DATABASE_CONFIG["dirname"],
                                       "%s.json"%user_dict["user"])

                print(user_path)
                if os.path.exists(user_path):
                    with open(user_path,"r") as f:
                        file_dict=json.load(f)
                        if file_dict["passwd"] == user_dict["passwd"]:
                            send_dict={"flag":True,"msg":"登陆成功","user":user_dict["user"]}
                            print(json.dumps(send_dict))
                            self.send_data(json.dumps(send_dict))
                            break
                        else:
                            send_dict = {"flag": False, "msg": "密码输入错误"}
                else:
                    send_dict={"flag":False,"msg":"用户名不存在"}
                print(json.dumps(send_dict))
                self.send_data(json.dumps(send_dict))
            while True:
                cmd=self.recv_data()
                if cmd == "send_file":
                    put(self)
                elif cmd == "recv_file":
                    get(self)
                elif cmd == "ls":
                    ls(self)
    server_socket=MyServer.SocketStart(setting.SERVER_ADDR)
def put(s):
    '''给客户端做put工作'''
    file_head = s.recv_data()
    file_head=json.loads(file_head)

    if not file_head["dstfile"]:
        file_head["dstfile"]=os.path.join(setting.SERVER_DIR,
                                          os.path.basename(file_head["srcfile"]))
    else:
        file_head["dstfile"] = os.path.join(setting.SERVER_DIR,
                                            os.path.basename(file_head["dstfile"]))
    s.send_data("ok")
    print(file_head)
    # 进度条
    rfi=s.recv_file_iter(file_head["dstfile"])
    size,filesize=rfi.__next__()
    for size in rfi:
        s.sendall_data(str(size/filesize))
        pass
    #
    # 接受完发送md5头部信息
    dst_md5=hash_factory.file_md5_factory(file_head["dstfile"])
    file_head["dstmd5"] = dst_md5
    file_head=json.dumps(file_head)
    print(file_head)
    s.sendall_data(file_head)


def get(s):
    '''给客户端做get工作'''
    file_head_dict=s.recv_data()
    file_head_dict=json.loads(file_head_dict)
    file_head_dict["srcfile"] = os.path.join(setting.SERVER_DIR,file_head_dict["srcfile"])
    if os.path.exists(file_head_dict["srcfile"]):
        file_head_dict.update({"flag":True,"msg":"源文件存在"})
        src_md5 = hash_factory.file_md5_factory(file_head_dict["srcfile"])
        file_head_dict["srcmd5"] = src_md5
    else:
        file_head_dict.update({"flag": False, "msg": "源文件不存在"})
    file_head=json.dumps(file_head_dict)
    s.send_data(file_head)

    if file_head_dict["flag"]:
        s.recv_data()
        sfi=s.send_file_iter(file_head_dict["srcfile"])
        for item in sfi:
            pass



def ls(s):
    '''给客户端做ls工作'''
    sight=s.recv_data()
    print(sight)
    import glob
    if sight == "?":
        dirlist=glob.glob1(s.message["pwd"],"*")
    else:
        dirlist = glob.glob1(s.message["pwd"],sight)
        print(sight)
    dirlist=json.dumps(dirlist)
    s.send_data(dirlist)
    pass



