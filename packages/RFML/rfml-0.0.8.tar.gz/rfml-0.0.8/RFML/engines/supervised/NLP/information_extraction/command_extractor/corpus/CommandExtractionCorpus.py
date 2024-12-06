from RFML.interface.ITrainingCorpus import ITrainingCorpus


class CommandExtractionItem:
    def __init__(self):
        self.text = ""
        self.ner_map = ""

    def to_json(self) -> {}:
        return {
            "text": self.text,
            "ner_map": self.ner_map,
        }

    def from_json(self, json: {}) -> any:
        self.text = json["ner"]["text"]  # corpus removed for training data call from train handler
        self.ner_map = json["ner"]["ner_map"]
        return self


class CommandExtractionCorpus(ITrainingCorpus):
    def __init__(self):
        self.ner_items = []

    def to_json(self) -> {}:
        items = {}
        for item in self.ner_items:
            data = {
                "text": item.text,
                "ner_map": item.ner_map,
            }
            items.update(data)
        return items

    def from_json(self, json: {}) -> any:
        for key in json["ner"]:
            item = CommandExtractionItem()
            item.text = key["text"]
            item.ner_map = key["ner_map"]
            self.ner_items.append(item)
        return self