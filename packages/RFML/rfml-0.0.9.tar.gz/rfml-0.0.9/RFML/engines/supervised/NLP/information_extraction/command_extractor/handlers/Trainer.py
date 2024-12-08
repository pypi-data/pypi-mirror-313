from RFML.core.Results import TrainResult
from RFML.corpus.Corpus import Corpus
from RFML.engines.supervised.NLP.information_extraction.command_extractor.corpus.CommandExtractionCorpus import \
    CommandExtractionCorpus
from RFML.engines.supervised.NLP.information_extraction.command_extractor.models.NER.IEBOTTrainer import IEBOTTrainer
from RFML.interface.ITrain import ITrain
from RFML.libs.utils import rf


class Trainer(ITrain[CommandExtractionCorpus]):
    def before_train(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: Corpus) -> TrainResult:
        return TrainResult("ss", 1, 1)

    def train(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: Corpus) -> TrainResult:
        data = corpus.training.read({"model": model_name})
        ner_data = rf.nlp.ner.generate_fnn_data(data)
        result = IEBOTTrainer.Train(ner_data, model_name, corpus.vector_db_home)
        if result[0]:
            return TrainResult(message=result[1])
        else:
            return TrainResult(message="Model training was not successful!")

    def after_train(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: Corpus) -> TrainResult:
        return TrainResult("ss", 1, 1)
