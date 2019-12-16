# class SingleTons(object):
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls,"_instance"):
#             cls._instance = super(SingleTons,cls).__new__(cls)
#         return cls._instance
#
# class Test01(SingleTons):
#     def __init__(self,name):
#         self.name = name
#
#
# aa=Test01("alex")
#
# bb=Test01("jack")
# print(aa.name)

class Test01:
    @classmethod
    def get_instance(cls,*args,**kwargs):
        if not hasattr(cls,"_instance"):
            cls._instance=cls(*args,**kwargs)

        return cls._instance

    def __init__(self,name):
        self.name = name

aa=Test01.get_instance("alex")

bb=Test01.get_instance("jack")
print(aa.name)