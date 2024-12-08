from RFML.interface.IPromptValidator import IPromptValidator
from RFML.prompt.PromptCash import PromptCash
from RFML.prompt.PromptQuery import PromptQuery


class Validator(IPromptValidator):
    # configure prompt_queries for validation check
    def configure_prompt_queries(self, model_name: str, prompt_query_list: list[PromptQuery]):
        pass

    # process input and store in prompt_queries for validation check
    def process_prompt_queries(self, model_name: str, pc: PromptCash, user_input: str):
        pass

    def format_prompt_queries(self, model_name: str, pc: PromptCash, valid_fields, user_input: str) -> str:
        pass
