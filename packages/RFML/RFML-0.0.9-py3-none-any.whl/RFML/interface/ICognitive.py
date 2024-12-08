from abc import ABC, abstractmethod

from RFML.core.Cognitive import Cognitive


class ICognitive(ABC):
    @abstractmethod
    def configure(self, cognitive: Cognitive):
        # raise NotImplementedError("Please implement IPrompt")
        pass
