#!/usr/bin/env python
#--coding: utf-8--

import hashlib
def hash_md5_factory(data):
    '''hash factory'''
    hashed = hashlib.md5()
    hashed.update(bytes(data, encoding="utf8"))
    data = hashed.hexdigest()
    return data

def hash_md5_iter_factory(type="bytes"):
    '''该函数用于迭代传入'''
    hashed = hashlib.md5()
    while True:
        data=yield
        if not data:
            break
        if type == "bytes":
            hashed.update(data)
        else:
            hashed.update(bytes(data, encoding="utf8"))
    data = hashed.hexdigest()
    yield data

def file_md5_factory(filename):
    hash_md5=hash_md5_iter_factory()
    hash_md5.__next__()
    with open(filename,"rb") as f:
        for line in f:
            hash_md5.send(line)

        md5_ret=hash_md5.__next__()
    return md5_ret



def hash_sha256_factory(data):
    '''hash factory'''
    hashed = hashlib.sha256()
    hashed.update(bytes(data, encoding="utf8"))
    data = hashed.hexdigest()
    return data

def hash_sha512_factory(data):
    '''hash factory'''
    hashed = hashlib.sha512()
    hashed.update(bytes(data, encoding="utf8"))
    data = hashed.hexdigest()
    return data