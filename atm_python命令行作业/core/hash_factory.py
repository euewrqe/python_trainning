import hashlib
def hash_factory(data):
    '''hash factory'''
    hashed = hashlib.md5()
    hashed.update(bytes(data, encoding="utf8"))
    data = hashed.hexdigest()
    return data