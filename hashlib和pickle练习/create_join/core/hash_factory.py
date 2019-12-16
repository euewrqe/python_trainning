import hashlib
def hash_md5_factory(data):
    '''hash factory'''
    hashed = hashlib.md5()
    hashed.update(bytes(data, encoding="utf8"))
    data = hashed.hexdigest()
    return data

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