from abc import ABC, abstractmethod

class Template(ABC):
  
    @abstractmethod
    def build_settings(self):
        pass

