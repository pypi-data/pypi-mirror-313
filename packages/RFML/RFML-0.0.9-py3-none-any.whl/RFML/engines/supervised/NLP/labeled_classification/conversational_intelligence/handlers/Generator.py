from RFML.core.Results import GenerateResult
from RFML.engines.supervised.NLP.information_extraction.command_extractor.corpus.CommandExtractionCorpus import \
    CommandExtractionCorpus
from RFML.interface.ITrainingCorpus import ITrainingCorpus
from RFML.interface.IGenerate import IGenerate, T


class Generator(IGenerate[CommandExtractionCorpus]):
    def before_generate(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: ITrainingCorpus):
        pass

    def generate(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: ITrainingCorpus) -> GenerateResult:
        pass

    def after_generate(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: ITrainingCorpus):
        pass
