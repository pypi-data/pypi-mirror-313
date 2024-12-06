from RFML.interface.ITrainingCorpus import ITrainingCorpus


class ConversationalIntelligenceCorpus(ITrainingCorpus):
    def __init__(self):
        self.tag = ""
        self.patterns = []
        self.response = []
        self.route = ""

    def to_json(self) -> {}:
        return {
            "tag": self.tag,
            "patterns": self.patterns,
            "response": self.response,
            "route": self.route,
        }

    def from_json(self, json: {}):
        # self.tag = json["tag"]
        # self.patterns = json["patterns"]
        # self.response = json["response"]
        # self.route = json["route"]
        return self
