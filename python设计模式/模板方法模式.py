from abc import abstractmethod,ABCMeta

class IOHandler:
    @abstractmethod
    def open_file(self,filename):
        pass

    @abstractmethod
    def get_content(self):
        pass

    @abstractmethod
    def close_file(self):
        pass

    def process(self,filename):
        self.open_file(filename)
        content=self.get_content()
        self.close_file()
        return content

