from enum import Enum


class TaskType(Enum):
    Train = 1
    Generate = 2
    Predict = 3
    Reload = 4
    Register = 5


class Interaction:
    session_id: str
    model: str  # for API model train
    task: TaskType
    input: str
    cancel_request: bool
    pass_request_length: int

    def __init__(
            self, session_id: str, model: str, task: TaskType, user_input: str, cancel_request=True,
            pass_request_length=15
    ):
        self.session_id = session_id
        self.model = model
        self.task = task
        self.input = user_input
        self.cancel_request = cancel_request
        self.pass_request_length = pass_request_length
