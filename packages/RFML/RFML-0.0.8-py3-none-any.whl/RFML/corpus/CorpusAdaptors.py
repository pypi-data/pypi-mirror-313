from RFML.corpus.adaptors.MongoDB import MongoDB
from RFML.interface.ICorpusAdaptor import ICorpusAdaptor


class CorpusAdaptors:
    @staticmethod
    def Mongo(url: str, db: str) -> ICorpusAdaptor:
        return MongoDB(url, db)
