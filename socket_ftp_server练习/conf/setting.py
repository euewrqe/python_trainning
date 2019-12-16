#!/usr/bin/env python
#--coding: utf-8--
import os,sys

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALL_CLIENT_DIR=os.path.join(BASE_DIR,"files/client_files")
SERVER_DIR=os.path.join(BASE_DIR,"files/server_files")

DATABASE_CONFIG={
    "type":"json",
    "dirname":os.path.join(BASE_DIR,"db")
}


SERVER_ADDR=("127.0.0.1",9999)