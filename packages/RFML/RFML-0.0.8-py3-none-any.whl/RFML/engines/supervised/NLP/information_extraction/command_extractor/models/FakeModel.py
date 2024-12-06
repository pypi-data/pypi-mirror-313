from RFML.core.Results import PredictResult, ResultType

valid = {
    "action": "book",
    "room": "JOBA",
    "start": "10am",
    "end": "11am",
}
not_valid = {
    "action": "book",
    "room": "",
    "start": "",
    "end": "",
}


class FakeModel:
    @staticmethod
    def predict(input_text):
        if input_text == "book a room" or input_text == "book":
            return PredictResult(
                label="book",
                probability=1.0,
                message=not_valid,
            )
        elif input_text == "JOBA1011" or input_text == "book a room JOBA from 10am to 11am":  # "book a room joba from 10am to 11pm":
            return PredictResult(
                label="book",
                probability=1.0,
                message=valid,
            )
        else:
            return PredictResult(
                label="book",
                probability=1.0,
                message="I’m here to help! Could you rephrase that question for me?",
                result_type=ResultType.do_not_understand
            )
