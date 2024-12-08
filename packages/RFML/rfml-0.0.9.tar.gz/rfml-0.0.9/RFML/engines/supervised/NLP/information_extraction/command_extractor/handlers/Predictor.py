from RFML.api.ServiceApi import ServiceApi
from RFML.core.ModelCache import ModelCache
from RFML.core.Results import PredictResult
from RFML.corpus.Corpus import Corpus
from RFML.engines.supervised.NLP.information_extraction.command_extractor.models.NER.IEBOT import IEBOT
from RFML.interface.IPredict import IPredict


class Predictor(IPredict):
    def __init__(self, model, mc: ModelCache, vector_db_home: str):
        self.mc = mc
        self.bot = self.mc.get(model) or IEBOT(model, vector_db_home)
        if not self.mc.get(model): self.mc.load(model, self.bot)

    def reload_model(self, model_name: str, corpus: Corpus) -> str:  # MC issue xx import ??
        try:
            self.bot = IEBOT(model_name, corpus.vector_db_home)
            self.mc.load(model_name, self.bot)
        except Exception as e:
            return str(e)

    def before_predict(self, model_name: str, input_text: str) -> str:
        # return input_text
        pass

    def predict(self, model_name: str, input_text: str, corpus: Corpus) -> PredictResult:
        # result= FakeModel.predict(input_text)
        # return result
        result = self.bot.predict(model_name, input_text)
        return result

    pr_info = [
        {'Id': 5000, 'Requestor': 'Imrose', 'Status': 'Pending'},
        {'Id': 5001, 'Requestor': 'Sajeeb', 'Status': 'Pending'},
        {'Id': 5002, 'Requestor': 'Salam', 'Status': 'Pending'},
    ]

    def after_predict(self, model_name: str, predict_result: PredictResult, service_api: ServiceApi) -> PredictResult:
        if predict_result.message["Action"].lower() == "show":
            predict_result.message = self.pr_info

        elif predict_result.message["Action"].lower() == "approve":
            for item in self.pr_info:
                pr_no = predict_result.message["PR"]
                if item['Id'] == int(pr_no):
                    item['Status'] = 'Approved'
                    predict_result.message = \
                        f"PR {predict_result.message['PR']} is approved successfully."
                    break
        elif predict_result.message["Action"].lower() == "disapprove":
            for item in self.pr_info:
                pr_no = predict_result.message["PR"]
                if item['Id'] == int(pr_no):
                    item['Status'] = 'Pending'
                    predict_result.message = \
                        f"PR {predict_result.message['PR']} is disapprove successfully."
                    break

        return predict_result

    def on_model_callback(self, predict_result: PredictResult) -> PredictResult:
        pass
