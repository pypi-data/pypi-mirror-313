from RFML.interface.ICorpusAdaptor import ICorpusAdaptor


class MemoryDB(ICorpusAdaptor):
    def read(self, collection: str, child: str, query: str, callback):
        pass

    def save(self, collection: str, child: str, value: {}) -> str:
        pass

    def update(self, collection: str, child: str, query: {}, value: {}) -> str:
        pass

    def push(self, collection: str, child: str, query: {}, value: {}) -> str:
        pass

    def delete(self, collection: str, child: str, query: {}) -> str:
        pass

    def empty(self, collection: str, child: str, query: {}) -> str:
        pass

    def is_empty(self, collection: str, query: {}) -> bool:
        pass
