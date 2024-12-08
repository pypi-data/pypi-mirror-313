from RFML.core.Cognitive import Cognitive, Handlers, Modules
from RFML.core.Meta import Meta, LearningType, CognitiveSkills, Algorithm, Intelligence, NN
from RFML.corpus.Corpus import Corpus
from RFML.corpus.CorpusAdaptors import CorpusAdaptors
from RFML.engines.supervised.NLP.labeled_classification.conversational_intelligence.handlers.Generator import Generator
from RFML.engines.supervised.NLP.labeled_classification.conversational_intelligence.handlers.Predictor import Predictor
from RFML.engines.supervised.NLP.labeled_classification.conversational_intelligence.handlers.Trainer import Trainer
from RFML.interface.ICognitive import ICognitive


class ConversationalIntelligence(ICognitive):
    corpus_url = ""

    def __init__(
            self, model="", corpus_url="mongodb://localhost:27017/", models_home=rf"C:\RFMLModels",
            modules: Modules = None
    ):
        self.corpus_url = corpus_url
        self.model = model
        self.modules = modules
        self.models_home = models_home

    def configure(self, cognitive: Cognitive):
        cognitive.model = self.model
        cognitive.purpose = "greetings bot"
        cognitive.gateway = True
        cognitive.handlers = Handlers(
            Predictor(self.model, self.models_home), Trainer(), Generator(), None
        )  # Validator()
        cognitive.corpus = Corpus(
            training_dataset=Corpus.templates.NLP.ConversationalIntelligenceCorpus,
            adaptor=CorpusAdaptors.Mongo(self.corpus_url, "cortex"),
            models_home=self.models_home
        )
        cognitive.modules = self.modules
        cognitive.meta = Meta(
            learning_type=LearningType.Supervised,
            cognitive_skills=CognitiveSkills.Classification,
            algorithm=Algorithm.Liner_Regression,
            intelligence=Intelligence.Knowledge_Discovery,
            NN=NN.FFN,
        )
