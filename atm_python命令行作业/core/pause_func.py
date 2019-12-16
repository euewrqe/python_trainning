def pause_func(func):
    '''
    业务暂停措施
    :param func:
    :return:
    '''
    def inner(*args,**kwargs):
        print("本业务暂不开放")
        return None
    return inner