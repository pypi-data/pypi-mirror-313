class PromptCash:
    validator_cash: any = {}
    missing_validator_attribute: str = ""
    last_prompt_query: str = ""
    last_user_input: str = ""

    def __init__(self, json: any):
        self.validator_cash = json["validator_cash"]
        self.missing_validator_attribute = json["missing_validator_attribute"]
        self.last_prompt_query = json["last_prompt_query"]
        self.last_user_input = json["last_user_input"]

    def to_json(self):
        return {
            "validator_cash": self.validator_cash,
            "missing_validator_attribute": self.missing_validator_attribute,
            "last_prompt_query": self.last_prompt_query,
            "last_user_input": self.last_user_input,
        }

    def set_cancel_prompt(self):
        for key, value in self.validator_cash.items():
            self.validator_cash[key] = "__canceled__"

    def set_pass_prompt(self):
        for key, value in self.validator_cash.items():
            if not self.validator_cash[key]: self.validator_cash[key] = "__passed__"
