import spacy
from RFML.core.Results import PredictResult, ResultType


class IEBOT:
    def __init__(self, model: str, vector_db_path: str):
        try:
            self.nlp = spacy.load(rf"{vector_db_path}\{model}")
        except Exception as e:
            print(e)

    def predict(self, model_name: str, sentence: str):
        if model_name == "rf-ce-flight_booking":
            return self.predict_flight(sentence)
        elif model_name == "rf-ce-pr_process":
            return self.predict_pr(sentence)

    def predict_pr(self, sentence: str):
        data = {}
        action = ""
        data_show = {"Action": "", "Time": ""}
        data_approve = {"Action": "", "PR": ""}

        doc = self.nlp(sentence)
        for ent in doc.ents:
            if ent.label_ == "Action": action = ent.text.lower()  # "Entity:ent.text, Label:ent.label_"
            data[ent.label_] = ent.text

        (data_show if action == "show" else data_approve).update(data)

        if len(doc.ents) > 0 and (action == "show" or action == "approve" or action == "disapprove") and \
                any(keyword in sentence for keyword in ["PR", "PRs"]):
            return PredictResult(label="pr_booking", message=data_show if action == "show" else data_approve)
        else:
            return PredictResult(
                result_type=ResultType.do_not_understand, label="pr_booking",
                message="The PR details are not clearly specified!"
            )

    def predict_flight(self, sentence: str):
        doc = self.nlp(sentence)
        data = {
            "Action": "",
            "Origin": "",
            "Destination": "",
            "Date": "",
            "Time": ""
        }
        for ent in doc.ents: data[ent.label_] = ent.text  # "Entity:ent.text, Label:ent.label_

        if len(doc.ents) > 0 and data["Action"] == "book" and "flight" in sentence:
            return PredictResult(label="flight_booking", message=data)
        else:
            return PredictResult(
                result_type=ResultType.do_not_understand, label="flight_booking",
                message="The booking details are not clearly specified!"
            )
