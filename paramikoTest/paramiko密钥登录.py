#!/usr/bin/env python
#--coding:utf-8--
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import paramiko

private_key=paramiko.RSAKey.from_private_key_file("id_rsa")

ssh=paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="10.0.0.20",port=22,username="euewrqe",pkey=private_key)
stdin,stdout,stderr=ssh.exec_command("awk 'BEGIN{print(\"hello world\")}'")
result=stdout.read()
print(result)
ssh.close()