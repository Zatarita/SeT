from saber.file.file_generic import FileGeneric
from abc import ABCMeta, abstractmethod
import os

"""
    FileSaberGeneric:
        Handles saber specific file information. FileGeneric's second abstraction.
"""


class SaberFileGeneric(FileGeneric, metaclass=ABCMeta):
    def __init__(self):
        FileGeneric.__init__(self)
        self.children = {}

    # -----------------------------------------------------Item I/O
    def importChild(self, name, data):
        self.children.update({name: data})

    def importChildren(self, data):
        self.children += data

    def exportChild(self, path, name):
        with open(path, "wb") as file:
            file.write(self.children[name].getData())

    def exportAll(self, path):
        for child in self.children.keys():
            try:
                os.mkdir(path)
            except:
                pass
            self.exportChild(path + "/" + child, child)

    def delete(self, name):
        self.children.pop(name)

    # -----------------------------------------------------Data Access
    def names(self):
        return list(self.children.keys())

    def childCount(self):
        return len(self.children)

    def childAtIndex(self, index):
        if index > len(self.children) or index == -1:
            return
        return list(self.children.values())[index]

    def find(self, item):
        for i in range(len(self.children)):
            if list(self.children.keys())[i] == item:
                return i
        return -1
