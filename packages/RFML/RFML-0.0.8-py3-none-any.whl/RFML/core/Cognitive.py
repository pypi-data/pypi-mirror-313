from RFML.core.CognitiveModule import CognitiveModule
from RFML.core.Meta import Meta
from RFML.corpus.Corpus import Corpus
from RFML.corpus.CorpusAdaptors import MongoDB
from RFML.interface.ICorpusAdaptor import ICorpusAdaptor
from RFML.interface.IPredict import IPredict
from RFML.interface.IPromptValidator import IPromptValidator


class Modules:
    modules: list[CognitiveModule]

    def __init__(self, modules: list[CognitiveModule]):
        self.modules = modules


class Handlers:
    predictor: IPredict
    trainer: any  # avoiding T ITrainer
    generator: any  # avoiding T  IGenerator
    validator: IPromptValidator
    corpus: ICorpusAdaptor = MongoDB

    def __init__(self, predict_handler: IPredict,
                 train_handler,
                 generator_handler,
                 validator_handler: IPromptValidator,
                 corpus_adaptor: ICorpusAdaptor = MongoDB):
        self.predictor = predict_handler
        self.trainer = train_handler
        self.generator = generator_handler
        self.validator = validator_handler
        self.corpus = corpus_adaptor


class AccessControl:
    user_id = "001"
    username = ""
    password = ""

    def login(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        pass


class Cognitive:
    model: str
    purpose: str
    corpus: Corpus
    modules: Modules = None
    handlers = Handlers
    meta = Meta
    access_control = AccessControl
    gateway = False

    def __init__(self, model: str, purpose: str, corpus: Corpus, meta: Meta, gateway=False):
        self.model = model
        self.purpose = purpose
        self.corpus = corpus
        self.meta = meta
        self.gateway = gateway
