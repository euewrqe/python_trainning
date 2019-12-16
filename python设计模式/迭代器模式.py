#链表

class MyList:
    def __init__(self,it):
        self.first = self.Node()
        self.last = self.Node()

        self.first.node = self.Node()


        self.last.node = self.first.node

        for i in it:

            self.last.node.data = i
            self.last.node.node = self.Node()
            self.last.node = self.last.node.node

    class ListIterator:
        def __init__(self,node):
            print("init")
            self.node = node
            input()
            self.node = node
        def __iter__(self):
            return self
        def __next__(self):
            if self.node.node:
                self.node = self.node.node
                return self.node.data
            else:
                raise StopIteration





    def show(self):
        self.middle = self.Node()
        self.middle.node = self.first.node
        while(self.middle.node.node):
            print(self.middle.node.data)
            self.middle.node = self.middle.node.node


    class Node:
        data=None
        node=None
        def __init__(self,data=None):
            pass

    def __iter__(self):
        return self.ListIterator(self.first)

    def append_item(self,data):
        self.middle = self.Node()
        self.middle.node = self.last.node
        print("---->",self.middle.node.data)
        self.last.node.data = data
        self.last.node.node = self.Node()
        self.last.node = self.last.node.node

    def __str__(self):
        return ",".join(map(str,self))


from collections import abc

class MyList:
    class Iterator:
        def __iter__(self):
            pass
        def __next__(self):
            pass

    def __init__(self):
        pass
    def __iter__(self):
        pass
names = ['alex','jack','array']
li = MyList(names)
li.append_item(50)
print(li)








