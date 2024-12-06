from abc import ABC, abstractmethod
from RFML.api.ServiceApi import ServiceApi
from RFML.core.Results import PredictResult
from RFML.corpus.Corpus import Corpus


class IPredict(ABC):
    @abstractmethod
    def reload_model(self, model_name: str, corpus: Corpus) -> str:
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def before_predict(self, model_name: str, input_text: str) -> str:
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def predict(self, model_name: str, input_text: str, corpus: Corpus) -> PredictResult:
        pass

    @abstractmethod
    def after_predict(self, model_name: str, predict_result: PredictResult, service_api: ServiceApi) -> PredictResult:
        pass

    @abstractmethod
    def on_model_callback(self, predict_result: PredictResult) -> PredictResult:
        pass
