import typing as t

from RFML.core.Conversation import Context, Conversation
from RFML.corpus.CorpusBase import CorpusCash
from RFML.engines.supervised.NLP.information_extraction.command_extractor.corpus.CommandExtractionCorpus import \
    CommandExtractionCorpus
from RFML.engines.supervised.NLP.labeled_classification.conversational_intelligence.corpus.ConversationalIntelligenceCorpus import \
    ConversationalIntelligenceCorpus
from RFML.interface.ITrainingCorpus import ITrainingCorpus
from RFML.interface.ICorpusAdaptor import ICorpusAdaptor
from RFML.prompt.PromptCash import PromptCash


class NLP:
    CommandExtractionCorpus = CommandExtractionCorpus()
    ConversationalIntelligenceCorpus = ConversationalIntelligenceCorpus()


class Templates:
    NLP = NLP()


T = t.TypeVar("T")


class Corpus:
    templates = Templates()  # ready data structure  text/entity_map

    training_corpus: ITrainingCorpus
    training: CorpusCash
    cognitive: CorpusCash  # JSON Data for text/entity_map
    context: CorpusCash
    conversation: CorpusCash
    prompt_cash: CorpusCash  # Current Model Mast fields
    do_not_understand: CorpusCash
    dialog: CorpusCash
    vector_db_home: str

    def __init__(self, training_dataset: ITrainingCorpus, adaptor: ICorpusAdaptor, models_home: str):
        self.training_corpus = training_dataset
        self.training = CorpusCash(adaptor, "cognitive", "corpus", Corpus.map_cognitive)
        self.cognitive = CorpusCash(adaptor, "cognitive", "corpus", Corpus.map_cognitive)
        self.conversation = CorpusCash(adaptor, "conversation", "", Corpus.map_conversation)
        self.context = CorpusCash(adaptor, "conversation", "context", Corpus.map_context)
        self.prompt_cash = CorpusCash(adaptor, "conversation", "prompt_cash", Corpus.map_prompt_cash)
        self.do_not_understand = CorpusCash(adaptor, "conversation", "do_not_understand", None)
        self.dialog = CorpusCash(adaptor, "conversation", "dialog", None)
        self.vector_db_home = models_home

    @staticmethod
    def map_cognitive(json, operation):
        # mod = importlib.import_module('Cognitive')
        from RFML.core.Cognitive import Cognitive
        cognitive = Cognitive(
            model="",
            purpose="",
            corpus=json[0]["corpus"],
            meta=None,
            gateway=False
        )
        return cognitive.corpus

    @staticmethod
    def map_prompt_cash(json, operation):
        if len(json[0]["prompt_cash"]) == 0:
            return None
        else:
            return PromptCash(json[0]["prompt_cash"])

    @staticmethod
    def map_context(json, operation):
        if len(json) == 0: return None
        return Context(
            label=json[0]["context"]["label"],
            model=json[0]["context"]["model"],
        )

    @staticmethod
    def map_conversation(json, operation):
        if json:
            return Conversation(
                session_id=json[0]["session_id"],
                user_id=json[0]["user_id"],
                date=json[0]["date"],
                time=json[0]["time"],
                last_access=json[0]["last_access"],
            )
        else:
            return None
