#!/usr/bin/env python
#--coding:utf-8--
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import paramiko

transport=paramiko.Transport(('10.0.0.20',22))
transport.connect(username="euewrqe",password="123456")

sftp=paramiko.SFTPClient.from_transport(transport)

sftp.put('huaji.jpg','./huaji.jpg')
transport.close()
