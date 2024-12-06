import re
import spacy
from RFML.core.Results import PredictResult, ResultType
from RFML.libs.utils import rf


class IEBOT:
    def __init__(self, model: str, vector_db_path: str):
        try:
            self.nlp = spacy.load(rf"{vector_db_path}\{model}")
        except Exception as e:
            print(e)

    def predict(self, sentence: str):
        if not rf.nlp.prompt.is_incomplete_booking(sentence):
        # if sentence == "book a":
            msg = "Please specify what do you want to book?"
            return PredictResult(
                result_type=ResultType.do_not_understand,
                label="book",
                probability=1.0,
                message=msg
            )

        doc = self.nlp(sentence)
        # Extract and print the entities
        data = {
            "Action": "",
            "Origin": "",
            "Destination": "",
            "Date": "",
            "Time": ""
        }
        for ent in doc.ents:
            # print(f"Entity: {ent.text}, Label: {ent.label_}")
            data[ent.label_] = ent.text

        if not data["Action"]:
            return PredictResult(
                result_type=ResultType.do_not_understand,
                label="book",
                probability=1.0,
                message="Booking information are not clear!"
            )

        if len(doc.ents) > 0:
            return PredictResult(
                label="flight_booking",
                probability=1.0,
                message=data,
                route=""
            )
        else:
            return PredictResult(
                result_type=ResultType.do_not_understand,
                label="book",
                probability=1.0,
                message="Booking information are not clear!"
            )
