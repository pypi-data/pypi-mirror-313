import typing as t
from abc import ABC, abstractmethod

from RFML.core.Results import GenerateResult
from RFML.interface.ITrainingCorpus import ITrainingCorpus

T = t.TypeVar("T")


class IGenerate(t.Generic[T], ABC):
    @abstractmethod
    def before_generate(self, model_name: str, training_corpus: T, corpus: ITrainingCorpus):
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def generate(self, model_name: str, training_corpus: T, corpus: ITrainingCorpus) -> GenerateResult:
        pass

    @abstractmethod
    def after_generate(self, model_name: str, training_corpus: T, corpus: ITrainingCorpus):
        pass
