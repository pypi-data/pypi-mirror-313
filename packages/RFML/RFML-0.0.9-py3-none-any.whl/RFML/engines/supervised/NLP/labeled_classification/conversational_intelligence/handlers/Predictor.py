from RFML.api.ServiceApi import ServiceApi
from RFML.core.Results import PredictResult
from RFML.corpus.Corpus import Corpus
from RFML.engines.supervised.NLP.labeled_classification.conversational_intelligence.models.FNN.FNNBOT import FNNBOT
from RFML.interface.IPredict import IPredict


class Predictor(IPredict):
    def __init__(self, model: str, vector_db_home: str):
        self.bot = FNNBOT(model, vector_db_home)

    def reload_model(self, model_name: str, corpus: Corpus) -> str:
        try:
            self.bot = FNNBOT(model_name, corpus.vector_db_home)
            self.bot.intents = corpus.training.read({"model": model_name})["intents"]
        except Exception as e:
            return str(e)

    def before_predict(self, model_name: str, input_text: str):
        # return input_text
        pass

    def predict(self, model_name: str, input_text: str, corpus: Corpus) -> PredictResult:
        # return FakeModel.predict(input_text)
        if not self.bot.intents:
            self.bot.intents = corpus.training.read({"model": model_name})["intents"]
        result = self.bot.predict(input_text, {"intents": self.bot.intents})

        return PredictResult(
            label=result[0], probability=1.0, message=result[2], route=result[1],
            result_type=result[3]
        )

    def after_predict(self, model_name: str, predict_result: PredictResult, service_api: ServiceApi) -> PredictResult:
        # why?
        return PredictResult(
            label="some_label",
            probability=1.0,
            message=predict_result.message,
        )

    def on_model_callback(self, predict_result: PredictResult) -> PredictResult:
        if predict_result.label == "sysinfo":
            result = {}
            from platform import uname
            result["OS"] = f"{uname().system} {uname().release}, {uname().version}"

            from psutil import virtual_memory  # pip install psutil
            result["Memory"] = f"{virtual_memory().total}"

            from datetime import datetime
            result["System Time"] = f"{datetime.now().astimezone().strftime('%H:%M:%S %z')}"

            from tzlocal import get_localzone  # pip install tzlocal
            result["Timezone"] = f"{get_localzone()}"

            return PredictResult(
                session_id=predict_result.session_id,
                label=predict_result.label,
                probability=0.0,
                message=result,
                route=""
            )
