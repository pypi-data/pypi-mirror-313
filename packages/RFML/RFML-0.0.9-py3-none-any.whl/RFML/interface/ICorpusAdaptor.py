from abc import ABC, abstractmethod


class ICorpusAdaptor(ABC):
    @abstractmethod
    def read(self, collection: str, child: str, query: str, callback):
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def save(self, collection: str, child: str, value: {}) -> str:
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def update(self, collection: str, child: str, query: {}, value: {}) -> str:
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def push(self, collection: str, child: str, query: {}, value: {}) -> str:
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def delete(self, collection: str, child: str, query: {}) -> str:
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def empty(self, collection: str, child: str, query: {}) -> str:
        # raise NotImplementedError("Please implement IPrompt")
        pass

    @abstractmethod
    def is_empty(self, collection: str, query: {}) -> bool:
        pass
