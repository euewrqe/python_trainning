from abc import abstractmethod,ABCMeta

#一部手机由多个零件组成，生产零件和组装零件分开，零件（CPU,内存，系统），组装的
# CPU()



# 抽象产品
class PhoneShell(metaclass=ABCMeta):
    @abstractmethod
    def show_shell(self):
        pass
class CPU(metaclass=ABCMeta):
    @abstractmethod
    def show_cpu(self):
        pass
class OS(metaclass=ABCMeta):
    @abstractmethod
    def show_os(self):
        pass
    pass
# 抽象工厂
class PhoneFactory(metaclass=ABCMeta):
    @abstractmethod
    def make_shell(self):
        pass

    @abstractmethod
    def make_cpu(self):
        pass

    @abstractmethod
    def make_os(self):
        pass

# 具体产品
class ApplePhoneShell(PhoneShell):
    pass
class AndroidPhoneShell(PhoneShell):
    pass

class AppleCPU(CPU):
    pass

class AndroidCPU(CPU):
    pass

class AppleOS(OS):
    pass
class AndroidOS(OS):
    pass

# 具体工厂
class IPhoneFactory(PhoneFactory):
    def make_shell(self):
        return ApplePhoneShell()

    def make_cpu(self):
        return AppleCPU()

    def make_os(self):
        return AppleOS()

class AndroidPhoneFactory(PhoneFactory):
    def make_shell(self):
        return AndroidPhoneShell()

    def make_cpu(self):
        return AndroidCPU()

    def make_os(self):
        return AndroidOS()

class OtherPhoneFactory(PhoneFactory):
    def make_shell(self):
        return AndroidPhoneShell()

    def make_cpu(self):
        return AppleCPU()

    def make_os(self):
        return AndroidOS()
# 客户端
def make_phone(factory):
    pass