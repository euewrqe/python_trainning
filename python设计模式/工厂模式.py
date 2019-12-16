from abc import abstractmethod,ABCMeta

#抽象产品
class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self):
        pass

#具体产品
class AliPayment(Payment):
    def pay(self):
        print("阿里支付")

class PaypalPayment(Payment):
    def pay(self):
        print("paypal支付")

class OtherPayment(Payment):
    def pay(self):
        print("其他支付")


#工厂
class Factory():
    def __init__(self,method):
        if method == "alipay":
            self.pay_obj = AliPayment()

        elif method == "paypalpay":
            self.pay_obj = PaypalPayment()

        elif method == "otherpay":
            self.pay_obj = OtherPayment()

    def pay(self):
        self.pay_obj.pay()


class AliPayFactory:
    def pay(self):
        obj = AliPayment()
        obj.pay()


class PaypalPayFactory:
    def pay(self):
        obj = PaypalPayment()
        obj.pay()

class OtherPayFactory:
    def pay(self):
        obj = PaypalPayment()
        obj.pay()

if __name__ == "__main__":
    pay_obj=PaypalPayment()   #只需要修改参数就能拿到不同的产品，每个类的出口函数统一
    pay_obj.pay()