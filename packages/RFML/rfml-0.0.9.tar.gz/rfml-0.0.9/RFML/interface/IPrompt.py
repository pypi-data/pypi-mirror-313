from abc import ABC, abstractmethod


class IPrompt(ABC):
    @abstractmethod
    def on_prompt_in(self, text_input: str) -> str:
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def on_prompt_out(self, text_input: str) -> str:
        # raise NotImplementedError("Please implement IPrompt")
        pass
