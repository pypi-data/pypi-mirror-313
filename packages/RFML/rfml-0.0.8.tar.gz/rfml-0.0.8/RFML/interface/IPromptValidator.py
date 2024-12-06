from abc import ABC, abstractmethod

from RFML.prompt.PromptCash import PromptCash


class IPromptValidator(ABC):

    @abstractmethod
    def configure_prompt_queries(self, prompt_queries_list: []):
        pass

    @abstractmethod
    def process_prompt_queries(self, pc: PromptCash, user_input: str):
        pass

    @abstractmethod
    def format_prompt_queries(self, pc: PromptCash, valid_fields, user_input: str):
        pass
