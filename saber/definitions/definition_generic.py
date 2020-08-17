from abc import ABCMeta, abstractmethod


class DefinitionGeneric(metaclass=ABCMeta):
    def __init__(self):
        self.type = ""
        self.data = None

    def load(self): pass

    def save(self): pass

    # -----------------------------------------------------Virtual Function **MUST OVERRIDE**
    @abstractmethod
    def compileData(self):
        pass

