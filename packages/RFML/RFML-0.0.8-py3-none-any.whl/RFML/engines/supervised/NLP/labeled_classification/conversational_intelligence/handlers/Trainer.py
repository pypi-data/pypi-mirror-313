from RFML.core.Results import TrainResult
from RFML.corpus.Corpus import Corpus
from RFML.engines.supervised.NLP.labeled_classification.conversational_intelligence.corpus.ConversationalIntelligenceCorpus import \
    ConversationalIntelligenceCorpus
from RFML.engines.supervised.NLP.labeled_classification.conversational_intelligence.models.FNN.FNNBOTTrainer import \
    FNNBOTTrainer
from RFML.interface.ITrain import ITrain


class Trainer(ITrain[ConversationalIntelligenceCorpus]):
    def before_train(self, model_name: str, training_corpus: ConversationalIntelligenceCorpus,
                     corpus: Corpus) -> TrainResult:
        return TrainResult("ss", 1, 1)

    def train(self, model_name: str, training_corpus: ConversationalIntelligenceCorpus, corpus: Corpus) -> TrainResult:
        data = corpus.training.read({"model": model_name})
        result = FNNBOTTrainer.Train(data, model_name, corpus.vector_db_home)
        if result[0]:
            return TrainResult(message=result[1])
        else:
            return TrainResult(message="Model training was not successful!")

    def after_train(self, model_name: str, training_corpus: ConversationalIntelligenceCorpus,
                    corpus: Corpus) -> TrainResult:
        return TrainResult("ss", 1, 1)
