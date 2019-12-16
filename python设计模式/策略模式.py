from abc import abstractmethod,ABCMeta
class Shopper(metaclass=ABCMeta):
    @abstractmethod
    def open_door(self):
        pass

class HaircutShopper(Shopper):
    def open_door(self):
        pass

class Super(Shopper):
    def open_door(self):
        pass

class CustomShopper(Shopper):
    def open_door(self):
        pass

class Option:
    def __init__(self,strategy):
        self.strategy = strategy()

    def open_door(self):
        self.strategy.open_door()

st=Option(CustomShopper)
st.open_door()