from abc import ABC, abstractmethod


class ITrainingCorpus(ABC):
    @abstractmethod
    def to_json(self) -> {}:
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def from_json(self, json: {}):
        # raise NotImplementedError("Please implement IPrompt")
        pass
