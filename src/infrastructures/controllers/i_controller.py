from abc import ABC, abstractmethod

class IController(ABC):

    @abstractmethod
    def run(self, *args):
        raise NotImplementedError