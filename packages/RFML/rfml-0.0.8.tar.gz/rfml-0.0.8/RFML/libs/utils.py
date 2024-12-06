from RFML.libs.NLP.CancelPrompt import CancelPrompt
from RFML.libs.NLP.Generator import Generator
from RFML.libs.core.DateTime import DateTime


class Nlp:
    ner = Generator()
    prompt = CancelPrompt()


class rf:
    datetime = DateTime()
    nlp = Nlp()
