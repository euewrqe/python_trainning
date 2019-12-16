#!/usr/bin/env python
#--coding: utf-8--

import os,sys
# 添加全局目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import client_api

from sys import argv

import optparse

'''client 127.0.0.1:9999 -u euewrqe -p 123456'''


parser=optparse.OptionParser(usage="ddddd")
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")
(options, args) = parser.parse_args()
print(options,args)


exit()

try:

    if len(argv)== 2:
        ip_addr = argv[1]
        print(ip_addr)
        client_api.client_trance(ip_addr)
    elif len(argv)> 2:
        ip_addr = argv[1]
        if argv.index("-p") and argv.index("-u"):
            username = argv[argv.index("-u") + 1]
            password = argv[argv.index("-p") + 1]
            client_api.client_trance(ip_addr,username,password)
        elif argv.index("-u"):
            username = argv[argv.index("-u") + 1]
            client_api.client_trance(ip_addr, username)
    else:
        client_api.client_trance()


except ValueError as e:
    pass
except Exception as e:
    from core import tools
    tools.make_color(e,"red")


client_api.client_trance()