from abc import ABC, abstractmethod
import re

class Separator(ABC):
    @abstractmethod
    def separator(self, string: str):
        pass

class DashSeparator(Separator):
    def separator(self, string: str):
        return bool(re.search(r'^[\n\s\-]+$', string))

class EmptyLineSeparator(Separator):
    def separator(self, string: str):
        return bool(re.search(r'^\n$', string))

def separators(line: str):
    return [ subclass().separator(line) 
        for subclass in Separator.__subclasses__() ]
