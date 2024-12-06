from RFML.interface.ICorpusAdaptor import ICorpusAdaptor


class CorpusBase:
    def __init__(self, corpus_adaptor: ICorpusAdaptor, collection: str, child: str, callback):  # base adapter same
        self.corpus_adaptor = corpus_adaptor
        self.collection = collection
        self.child = child
        self.callback = callback

    def read(self, query: str):
        return self.corpus_adaptor.read(self.collection, self.child, query, self.callback)

    def save(self, value: {}):
        self.corpus_adaptor.save(self.collection, self.child, value)

    def update(self, query: {}, value: {}):
        self.corpus_adaptor.update(self.collection, self.child, query, value)

    def push(self, query: {}, value: {}):
        self.corpus_adaptor.push(self.collection, self.child, query, value)

    def delete(self, query: str):
        self.corpus_adaptor.delete(self.collection, self.child, query)

    def empty(self):
        self.corpus_adaptor.empty(self.collection, self.child, "")

    def is_empty(self):
        if self.corpus_adaptor.is_empty(self.collection, ""):
            return True
        else:
            return False


class CorpusCash(CorpusBase):
    operation = ""
    corpus_adaptor = any
    collection = ""
    child = ""
    callback = any

    def __init__(self, corpus_adaptor: ICorpusAdaptor, collection: str, child: str, callback):
        super().__init__(corpus_adaptor, collection, child, callback)
        self.corpus_adaptor = corpus_adaptor
        self.collection = collection
        self.child = child
        self.callback = callback

    def update(self, session_id, data):
        if self.child == "prompt_cash":
            super().update({"session_id": session_id}, {"prompt_cash": data})
        elif self.child == "context":
            super().update({"session_id": session_id}, {"context": data})
        elif self.child == "":  # conversation
            super().update({"session_id": session_id}, data)

    def push(self, session_id, data):
        if self.child == "do_not_understand":
            super().push({"session_id": session_id}, {"do_not_understand": data})
        elif self.child == "dialog":
            super().push({"session_id": session_id}, {"dialogs": data})
