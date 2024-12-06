from enum import Enum


class ResultType(Enum):
    model_default = 0
    do_not_understand = 1


class PredictResult:
    session_id: str
    model: str
    label: str
    probability: float
    message: any
    route: str
    result_type: ResultType
    input_text: str

    def __init__(self, session_id="", label="", probability=0.0, message="", route="",
                 result_type: ResultType = ResultType.model_default, input_text: str = ""):
        self.session_id = session_id
        self.model = ""
        self.label = label
        self.probability = probability
        self.message = message
        self.route = route
        self.result_type = result_type
        self.input_text = input_text

    def to_json(self):
        return {
            "session_id": self.session_id,
            "model": self.model,
            "label": self.label,
            "probability": self.probability,
            "message": self.message,
            "route": self.route,
            "result_type": self.result_type,
            "input_text": self.input_text
        }


class TrainResult:
    message = ""
    inference = 1
    accuracy = 1

    def __init__(self, message, inference=0.1, accuracy=0.8):
        self.message = message
        self.inference = inference
        self.accuracy = accuracy


class GenerateResult:
    label = ""
    message = 1

    def __init__(self, label, message):
        self.label = label
        self.message = message
