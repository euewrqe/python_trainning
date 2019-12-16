from abc import abstractmethod,ABCMeta

#抽象产品
class Watch(metaclass=ABCMeta):
    @abstractmethod
    def show(self):
        pass

#具体产品
class XiaoBangWatch(Watch):
    def show(self):
        print("肖邦表")

class LaoLiShiWatch(Watch):
    def show(self):
        print("劳力士表")



#工厂
class Factory():
    def __init__(self,method):
        if method == "xiaobang":
            self.watch_obj = XiaoBangWatch()

        elif method == "laolishi":
            self.watch_obj = LaoLiShiWatch()

    def show(self):
        self.watch_obj.show()

if __name__ == "__main__":
    watch_obj=Factory('xiaobang')   #只需要修改参数就能拿到不同的产品，每个类的出口函数统一
    watch_obj.show()