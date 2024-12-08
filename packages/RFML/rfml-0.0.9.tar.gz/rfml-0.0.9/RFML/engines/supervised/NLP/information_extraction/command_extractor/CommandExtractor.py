from RFML.core.Cognitive import Cognitive, Handlers, Modules
from RFML.core.Meta import Meta, LearningType, CognitiveSkills, Algorithm, Intelligence, NN
from RFML.core.ModelCache import ModelCache
from RFML.corpus.Corpus import Corpus
from RFML.corpus.CorpusAdaptors import CorpusAdaptors
from RFML.engines.supervised.NLP.information_extraction.command_extractor.handlers.Generator import Generator
from RFML.engines.supervised.NLP.information_extraction.command_extractor.handlers.Predictor import Predictor
from RFML.interface.ICognitive import ICognitive
from .handlers.Trainer import Trainer
from .handlers.Validator import Validator
from .models.NER.IEBOT import IEBOT


class CommandExtractor(ICognitive):
    corpus_url = ""
    mc = ModelCache()

    def __init__(
            self, model="", corpus_url="mongodb://localhost:27017/", models_home=rf"C:\RFMLModels",
            modules: Modules = None
    ):
        self.corpus_url = corpus_url
        self.model = model
        self.models_home = models_home

        # loading model beforehand to avoid response delay during chat
        self.mc.load(model, IEBOT(model, models_home))

    def configure(self, cognitive: Cognitive):
        cognitive.model = self.model
        cognitive.purpose = "extract information from voice/text command"
        cognitive.handlers = Handlers(
            Predictor(self.model, self.mc, self.models_home), Trainer(), Generator(), Validator()
        )
        cognitive.corpus = Corpus(
            training_dataset=Corpus.templates.NLP.CommandExtractionCorpus,
            adaptor=CorpusAdaptors.Mongo(self.corpus_url, "cortex"),
            models_home=self.models_home
        )
        cognitive.meta = Meta(
            learning_type=LearningType.Supervised,
            cognitive_skills=CognitiveSkills.Classification,
            algorithm=Algorithm.Liner_Regression,
            intelligence=Intelligence.Knowledge_Discovery,
            NN=NN.FFN,
        )
