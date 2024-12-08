import typing as t
from abc import ABC, abstractmethod

from RFML.core.Results import TrainResult
from RFML.corpus.Corpus import Corpus
from RFML.interface.ITrainingCorpus import ITrainingCorpus

T = t.TypeVar("T")


class ITrain(t.Generic[T], ABC):
    @abstractmethod
    def before_train(self, model_name: str, training_corpus: T, corpus: Corpus) -> TrainResult:
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def train(self, model_name: str, training_corpus: T, corpus: Corpus) -> TrainResult:
        pass

    @abstractmethod
    def after_train(self, model_name: str, training_corpus: T, corpus: Corpus) -> TrainResult:
        pass
