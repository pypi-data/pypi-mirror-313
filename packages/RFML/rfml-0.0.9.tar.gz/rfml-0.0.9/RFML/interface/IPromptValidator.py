from abc import ABC, abstractmethod

from RFML.core.Results import PromptProcessResult
from RFML.prompt.PromptCash import PromptCash


class IPromptValidator(ABC):

    @abstractmethod
    def configure_prompt_queries(self, model_name: str, prompt_queries_list: []):
        pass

    @abstractmethod
    def process_prompt_queries(self, model_name: str, pc: PromptCash, user_input: str) -> PromptProcessResult:
        pass

    @abstractmethod
    def format_prompt_queries(self, model_name: str, pc: PromptCash, valid_fields, user_input: str):
        pass
