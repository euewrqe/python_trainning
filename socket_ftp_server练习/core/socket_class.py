#!/usr/bin/env python
#--coding: utf-8--
import socketserver
import socket
from core import hash_factory
'''
socket类重构
'''
# 发送过去的内容一定要回复
# 指定一次传输多少
RECV_SIZE=1024

# 报头形式
HEAD={
    "size":None,
}

# 服务段socket重构

class NormalSocketServer(socketserver.BaseRequestHandler):
    '''
    此类用于封装socketserver的BaseRequestHandler类，用于简化收发消息的操作
    自定义发送和接收
    '''

    def handle(self):
        '''
        交互句柄
        :return:
        '''
        pass

    def send_data(self, string, sd_type="string",encoding="utf-8"):
        '''
        此函数是服务器发送数据函数，接收字符串，自动转换成字节，并发送给客户端
        :param string: 接受字符串
        '''
        if sd_type == "string":
            self.conn.sendall(bytes(string, encoding=encoding))
        elif sd_type == "bytes":
            self.conn.sendall(string)


    def recv_data(self, buff=RECV_SIZE, rt_type="string",encoding="utf-8"):
        '''
        此函数用于接收客户端发来的字节，默认缓冲数1024，返回字符串给变量
        :param buff:   缓冲数
        :return:   字符串
        '''
        string=None
        if rt_type == "string":
            string = str(self.conn.recv(buff), encoding=encoding)
        elif rt_type == "bytes":
            string = self.conn.recv(buff)

        return string

    def sendmore_data(self,string,sd_type="string",encoding="utf-8"):
        '''
        此函数用于解决粘包问题,对应recvmore_data
        :param string: 默认接收字符串
        :param rt_type:
        :return:
        '''
        sd_data_size=str(len(string))
        self.send_data(sd_data_size,encoding=encoding)
        print(self.recv_data())

        self.send_data(string,sd_type=sd_type)
        self.recv_data()

    def recvmore_data(self,once_buff=RECV_SIZE, rt_type="string",encoding="utf-8"):
        '''
        此函数用于解决粘包问题
        :param rt_type:
        :return:
        '''
        rt_data_size=self.recv_data(once_buff,encoding=encoding)
        rt_data_size = int(rt_data_size)
        self.send_data("ok")

        rt_data = b""
        while len(rt_data) < rt_data_size:
            # 只需要返回bytes,一次性转换
            rt_data += self.recv_data(once_buff, rt_type="bytes")
        self.send_data("ok")

        if rt_type == "string":
            rt_data = str(rt_data, encoding="utf-8")
        elif rt_type == "bytes":
            rt_data = rt_data
        return rt_data

    def sendall_data(self,string,sd_type="string",encoding="utf-8"):
        import json, struct
        sd_data_size = len(string)
        head = {
            "size":sd_data_size
        }
        head = bytes(json.dumps(head), encoding="utf8")
        head_size = struct.pack("i", len(head))
        self.send_data(head_size, sd_type="bytes",encoding=encoding)
        self.recv_data()
        self.send_data(head, sd_type="bytes",encoding=encoding)
        self.recv_data()
        self.send_data(string,sd_type,encoding=encoding)

        self.recv_data()

    def recvall_data(self,once_buff=RECV_SIZE, rt_type="string",encoding="utf-8"):
        '''此函数解决更多粘包问题'''
        import json,struct
        #第一次接收报头长度
        head_size=self.recv_data(once_buff,rt_type="bytes",encoding=encoding)
        head_size=struct.unpack("i",head_size)[0]
        self.send_data("ddd")
        #第二次接收报头，拿到报头中数据大小
        head=b""
        while len(head)<head_size:
            head+=self.recv_data(once_buff,rt_type="bytes",encoding=encoding)
        head=str(head,encoding="utf8")
        self.send_data("ddd")
        head=json.loads(head)
        #第三次接收主体内容
        rt_data_size = head["size"]
        rt_data=b""

        while len(rt_data)<rt_data_size:
            rt_data+=self.recv_data(once_buff,rt_type="bytes",encoding=encoding)
        self.send_data("ok")
        if rt_type == "string":
            rt_data = str(rt_data, encoding="utf-8")
        elif rt_type == "bytes":
            rt_data = rt_data
        return rt_data
    @classmethod
    def SocketStart(cls,address):
        server = socketserver.ThreadingTCPServer(address, cls)
        server.serve_forever()


# 客户端socket重构
class NormalSocketClient(socket.socket):
    '''
    此类为socket的派生类，简化connect操作，send和recv操作，关闭操作
    构造函数直接输入ip和地址就连接了
    '''
    def __init__(self,address):
        #此操作继承父级构造函数，创建对象时，相当于socket.socket()
        super(NormalSocketClient,self).__init__(family=2, type=1, proto=0, fileno=None)
        self.connect(address)
        pass
    def send_data(self,string,sd_type="string",encoding="utf-8"):
        '''
        此函数发送数据专用,默认接收字符串
        :param string: 默认接收字符串
        :param recv_type: 可以选择接收类型：string(字符串)/bytes(字节)
        '''
        if sd_type=="string":
            self.sendall(bytes(string,encoding=encoding))
        elif sd_type=="bytes":
            self.sendall(string)

    def recv_data(self,buff=RECV_SIZE,rt_type="string",encoding="utf-8"):
        '''
        此函数用于接收数据，默认返回字符串
        :param buff:   接收的大小
        :param rt_type:   接收后返回的类型：string/bytes
        :return:     默认返回string
        '''
        rt_data=None
        if rt_type=="string":
            rt_data=str(self.recv(buff),encoding=encoding)
        elif rt_type=="bytes":
            rt_data=self.recv(buff)
        return rt_data

    def sendmore_data(self,string,sd_type="string",encoding="utf-8"):
        '''
        此函数用于解决粘包问题,对应recvmore_data
        :param string: 默认接收字符串
        :param rt_type:
        :return:
        '''
        sd_data_size=str(len(string))
        self.send_data(sd_data_size)
        self.recv_data()

        self.send_data(string,sd_type=sd_type)
        self.recv_data()

    def recvmore_data(self,once_buff=RECV_SIZE,rt_type="string",encoding="utf-8"):
        '''
        此函数用于解决粘包问题
        :param once_buff: 一次接受多少buff
        :param rt_type:    接收后返回的类型：string/bytes
        :return:
        '''
        #接受大小

        rt_data_size=int(self.recv_data(once_buff))
        self.send_data("ok")

        rt_data=b""
        while len(rt_data)<rt_data_size:
            #只需要返回bytes,一次性转换
            rt_data+=self.recv_data(once_buff,rt_type="bytes")
        self.send_data("ok")
        if rt_type == "string":
            rt_data=str(rt_data,encoding=encoding)
        elif rt_type == "bytes":
            rt_data = rt_data
        return rt_data

    def sendall_data(self,string,sd_type="string",encoding="utf-8",sd_data_size=None):
        '''此函数解决更多粘包问题
        先发包头的长度

        '''
        import json,struct
        if not sd_data_size:
            sd_data_size = len(string)
        head = {
            "size": sd_data_size
        }
        head=bytes(json.dumps(head),encoding=encoding)
        head_size=struct.pack("i",len(head))
        self.send_data(head_size,sd_type="bytes")
        self.recv_data(RECV_SIZE)
        self.send_data(head,sd_type="bytes")
        self.recv_data(RECV_SIZE)
        self.send_data(string,sd_type=sd_type)
        #结束标识
        self.recv_data()


        pass
    def recvall_data(self,once_buff=RECV_SIZE,rt_type="string",encoding="utf-8"):
        '''此函数解决更多粘包问题'''
        import json, struct
        # 第一次接收报头长度
        head_size = self.recv_data(RECV_SIZE, rt_type="bytes")
        head_size = struct.unpack("i", head_size)[0]
        self.send_data("ddd")
        # 第二次接收报头，拿到报头中数据大小
        head = b""
        while len(head) < head_size:
            head += self.recv_data(once_buff, rt_type="bytes")
        head = str(head, encoding=encoding)
        self.send_data("ddd")
        head = json.loads(head)
        # 第三次接收主体内容
        rt_data_size = head["size"]
        rt_data = b""
        while len(rt_data) < rt_data_size:
            rt_data += self.recv_data(once_buff, rt_type="bytes")
        self.send_data("ok")
        if rt_type == "string":
            rt_data = str(rt_data, encoding=encoding)
        elif rt_type == "bytes":
            rt_data = rt_data
        return rt_data
    def __del__(self):
        self.close()

# 文件传输
import os,struct,json
class MySocketServer(NormalSocketServer):
    '''文件传输类'''
    def send_file(self, filename,encoding="utf-8"):
        '''
        为了统一，任何文件都以bytes格式打开
        '''
        mode = None
        # mode = "r" if type == "string" else mode = "rb"
        mode = "rb"
        file_size=os.path.getsize(filename)

        head={
            "size":file_size
        }
        head=bytes(json.dumps(head),encoding="utf-8")

        head_size=struct.pack("i",len(head))
        self.send_data(head_size,sd_type="bytes")
        print(self.recv_data())
        self.send_data(head,sd_type="bytes")

        #断点续传

        diff_dict=self.recv_data()  # {"rt_size": 23314554, "rt_md5": "df04980be4eee1173333b7e2d2a72a9f"}
        diff_dict=json.loads(diff_dict)
        print(diff_dict)
        if file_size <diff_dict["rt_size"]:

            rt_size = 0
            with open(diff_dict["dst_file"],"w") as f:
                f.truncate()
        else:
            rt_size = diff_dict["rt_size"]
        self.send_data(str(rt_size))
        print(self.recv_data())

        with open(filename, mode) as f:
            f.seek(rt_size)
            for line in f:
                self.sendall_data(line, "bytes")

        # self.recv_data()

    def send_file_iter(self, filename,encoding="utf-8"):
        '''
        迭代发送
        '''
        mode = None
        # mode = "r" if type == "string" else mode = "rb"
        mode = "rb"
        file_size=os.path.getsize(filename)

        head={
            "size":file_size
        }
        head=bytes(json.dumps(head),encoding="utf-8")

        head_size=struct.pack("i",len(head))
        self.send_data(head_size,sd_type="bytes")
        self.recv_data()
        print(file_size)
        self.send_data(head,sd_type="bytes")

        #断点续传

        diff_dict=self.recv_data()  # {"rt_size": 23314554, "rt_md5": "df04980be4eee1173333b7e2d2a72a9f"}
        diff_dict=json.loads(diff_dict)
        print(diff_dict)
        print(file_size,diff_dict["rt_size"])
        if file_size <diff_dict["rt_size"]:

            rt_size = 0
            with open(diff_dict["dst_file"],"w") as f:
                f.truncate()
        else:
            rt_size = diff_dict["rt_size"]
        self.send_data(str(rt_size))
        print(self.recv_data())

        with open(filename, mode) as f:
            f.seek(rt_size)
            for line in f:
                self.sendall_data(line, "bytes")
                yield

        # self.recv_data()

    def recv_file_iter(self,filename,once_buff=RECV_SIZE,encoding="utf-8"):
        '''服务段的recv'''
        mode = None
        mode = "ab"

        # 第一次接收报头长度
        head_size = self.recv_data(RECV_SIZE, rt_type="bytes")
        head_size = struct.unpack("i", head_size)[0]
        print(head_size)
        self.send_data("ok")
        #第二次接收报头，拿到报头中数据大小
        head = b""
        while len(head) < head_size:
            head += self.recv_data(once_buff, rt_type="bytes")
        head = str(head, encoding=encoding)
        print(head)
        head = json.loads(head)
        # 第三次接收主体内容
        file_size = head["size"]
        rt_data = b""
        # 断点续传
        if os.path.exists(filename):
            rt_size = os.path.getsize(filename)

            file_md5 = hash_factory.file_md5_factory(filename)
        else:
            rt_size = 0
            file_md5 = None
        # 校验文件内容


        diff_dict={
            "dst_file":filename,
            "rt_size":rt_size,
            "rt_md5":file_md5
        }
        diff_dict=json.dumps(diff_dict)

        self.send_data(diff_dict)

        rt_size = self.recv_data()
        print(rt_size,file_size)
        self.send_data("ok")
        rt_size = int(rt_size)
        print(rt_size,file_size)
        yield rt_size,file_size
        with open(filename, mode) as f:
            while rt_size<file_size:
                rt_data=self.recvall_data(once_buff,"bytes")
                rt_size += len(rt_data)
                f.write(rt_data)
                yield rt_size



        # self.send_data("ok")

    def recv_file(self,filename,once_buff=RECV_SIZE,encoding="utf-8"):
        '''服务段的recv'''
        mode = None
        mode = "ab"

        # 第一次接收报头长度
        head_size = self.recv_data(RECV_SIZE, rt_type="bytes")
        head_size = struct.unpack("i", head_size)[0]
        print("---",head_size)
        self.send_data("ok")
        #第二次接收报头，拿到报头中数据大小
        head = b""
        while len(head) < head_size:
            head += self.recv_data(once_buff, rt_type="bytes")
        head = str(head, encoding=encoding)

        head = json.loads(head)
        print(head)
        # 第三次接收主体内容
        file_size = head["size"]
        rt_data = b""
        # 断点续传
        if os.path.exists(filename):
            rt_size = os.path.getsize(filename)

            file_md5 = hash_factory.file_md5_factory(filename)
        else:
            rt_size = 0
            file_md5 = None
        # 校验文件内容


        diff_dict={
            "dst_file":filename,
            "rt_size":rt_size,
            "rt_md5":file_md5
        }
        diff_dict=json.dumps(diff_dict)
        print(diff_dict)
        self.send_data(diff_dict)
        rt_size = self.recv_data()
        print(rt_size,file_size)
        self.send_data("ok")
        rt_size = int(rt_size)
        with open(filename, mode) as f:
            while rt_size<file_size:
                rt_data=self.recvall_data(once_buff,"bytes")
                rt_size += len(rt_data)
                f.write(rt_data)



        # self.send_data("ok")



class MySocketClient(NormalSocketClient):
    '''文件传输类'''

    def send_file(self, filename,encoding="utf-8"):
        '''
        为了统一，任何文件都以bytes格式打开
        '''
        mode = None
        # mode = "r" if type == "string" else mode = "rb"
        mode = "rb"
        file_size=os.path.getsize(filename)

        head={
            "size":file_size
        }
        head=bytes(json.dumps(head),encoding="utf-8")

        head_size=struct.pack("i",len(head))
        self.send_data(head_size,sd_type="bytes")
        print(self.recv_data())
        self.send_data(head,sd_type="bytes")

        #断点续传

        diff_dict=self.recv_data()  # {"rt_size": 23314554, "rt_md5": "df04980be4eee1173333b7e2d2a72a9f"}
        diff_dict=json.loads(diff_dict)
        print(diff_dict)
        if file_size <diff_dict["rt_size"]:

            rt_size = 0
            with open(diff_dict["dst_file"],"w") as f:
                f.truncate()
        else:
            rt_size = diff_dict["rt_size"]
        self.send_data(str(rt_size))
        print(self.recv_data())

        with open(filename, mode) as f:
            f.seek(rt_size)
            for line in f:
                self.sendall_data(line, "bytes")

        # self.recv_data()

    def send_file_iter(self, filename,encoding="utf-8"):
        '''
        为了统一，任何文件都以bytes格式打开
        '''
        mode = None
        # mode = "r" if type == "string" else mode = "rb"
        mode = "rb"
        file_size=os.path.getsize(filename)

        head={
            "size":file_size
        }
        head=bytes(json.dumps(head),encoding="utf-8")

        head_size=struct.pack("i",len(head))
        self.send_data(head_size,sd_type="bytes")
        print(self.recv_data())
        self.send_data(head,sd_type="bytes")

        #断点续传

        diff_dict=self.recv_data()  # {"rt_size": 23314554, "rt_md5": "df04980be4eee1173333b7e2d2a72a9f"}
        diff_dict=json.loads(diff_dict)
        print(diff_dict)
        if file_size <diff_dict["rt_size"]:

            rt_size = 0
            with open(diff_dict["dst_file"],"w") as f:
                f.truncate()
        else:
            rt_size = diff_dict["rt_size"]
        self.send_data(str(rt_size))
        print(self.recv_data())

        with open(filename, mode) as f:
            f.seek(rt_size)
            for line in f:
                self.sendall_data(line, "bytes")
                yield

        # self.recv_data()
    def recv_file_iter(self,filename,once_buff=RECV_SIZE,encoding="utf-8"):
        '''服务段的recv'''
        mode = None
        mode = "ab"

        # 第一次接收报头长度
        head_size = self.recv_data(RECV_SIZE, rt_type="bytes")
        head_size = struct.unpack("i", head_size)[0]
        print(head_size)
        self.send_data("ok")
        #第二次接收报头，拿到报头中数据大小
        head = b""
        while len(head) < head_size:
            head += self.recv_data(once_buff, rt_type="bytes")
        head = str(head, encoding=encoding)
        print(head)
        head = json.loads(head)
        # 第三次接收主体内容
        file_size = head["size"]
        rt_data = b""
        # 断点续传
        if os.path.exists(filename):
            rt_size = os.path.getsize(filename)

            file_md5 = hash_factory.file_md5_factory(filename)
        else:
            rt_size = 0
            file_md5 = None
        # 校验文件内容


        diff_dict={
            "dst_file":filename,
            "rt_size":rt_size,
            "rt_md5":file_md5
        }
        diff_dict=json.dumps(diff_dict)

        self.send_data(diff_dict)

        rt_size = self.recv_data()
        print(rt_size,file_size)
        self.send_data("ok")
        rt_size = int(rt_size)
        yield rt_size,file_size
        with open(filename, mode) as f:
            while rt_size<file_size:
                rt_data=self.recvall_data(once_buff,"bytes")
                rt_size += len(rt_data)
                f.write(rt_data)
                yield rt_size



        # self.send_data("ok")

    def recv_file(self,filename,once_buff=RECV_SIZE,encoding="utf-8"):
        '''服务段的recv'''
        mode = None
        mode = "ab"

        # 第一次接收报头长度
        head_size = self.recv_data(RECV_SIZE, rt_type="bytes")
        head_size = struct.unpack("i", head_size)[0]
        print("---",head_size)
        self.send_data("ok")
        #第二次接收报头，拿到报头中数据大小
        head = b""
        while len(head) < head_size:
            head += self.recv_data(once_buff, rt_type="bytes")
        head = str(head, encoding=encoding)

        head = json.loads(head)
        print(head)
        # 第三次接收主体内容
        file_size = head["size"]
        rt_data = b""
        # 断点续传
        if os.path.exists(filename):
            rt_size = os.path.getsize(filename)

            file_md5 = hash_factory.file_md5_factory(filename)
        else:
            rt_size = 0
            file_md5 = None
        # 校验文件内容


        diff_dict={
            "dst_file":filename,
            "rt_size":rt_size,
            "rt_md5":file_md5
        }
        diff_dict=json.dumps(diff_dict)
        print(diff_dict)
        self.send_data(diff_dict)
        rt_size = self.recv_data()
        print(rt_size,file_size)
        self.send_data("ok")
        rt_size = int(rt_size)
        with open(filename, mode) as f:
            while rt_size<file_size:
                rt_data=self.recvall_data(once_buff,"bytes")
                rt_size += len(rt_data)
                f.write(rt_data)



        # self.send_data("ok")



