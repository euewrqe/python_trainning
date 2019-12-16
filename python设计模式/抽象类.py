from abc import abstractmethod,ABCMeta

class Animal(metaclass=ABCMeta):   #抽象基类
    @abstractmethod
    def walk(self):      #抽象基类的抽象方法，类Dog继承该类时，如果要调用实例化Dog类必须重写该函数
        pass
    def other(self):    #抽象基类的非抽象方法
        print("其他")
class Dog(Animal):
    def walk(self):
        print("小狗在走路")
class Cat(Animal):    #
    pass
d1 = Dog()  #可执行
d1.walk()
c1 = Cat()   #报错