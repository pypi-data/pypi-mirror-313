from RFML.libs.NLP.NERGen import ExtractionCorpus, Entity, CorpusData


class Generator:
    def generate_fnn_data(self, json_data):
        corpus = ExtractionCorpus()
        for item in json_data['ner']:
            text = item['text']
            ner_map = item['ner_map']
            entity_list = []
            for key, value in ner_map.items():
                entity_list.append(Entity(value, key))

            corpus.add(CorpusData(text, entity_list))
        return corpus.get()
