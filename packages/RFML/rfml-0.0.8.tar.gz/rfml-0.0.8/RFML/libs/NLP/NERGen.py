from enum import Enum


class NER(Enum):
    PERSON = 1
    NORP = 2
    GPE = 3
    ORG = 4


class Entity:
    def __init__(self, entity, label):
        self.entity = entity
        self.label = label


class CorpusData:
    def __init__(self, text, entities):
        self.text = text
        self.entities = entities


class ExtractionCorpus:
    def __init__(self):
        self.__dataset_list = []

    def add(self, dataset: CorpusData):
        entity_map_list = []
        for item in dataset.entities:
            entity_map = {"entity": item.entity, "label": item.label}
            entity_map_list.append(entity_map)

        nar_entities_map = {"entities": self.__generate_data(dataset.text, entity_map_list)}
        ner = (dataset.text, nar_entities_map)
        self.__dataset_list.append(ner)

    def get(self):
        return self.__dataset_list

    def __generate_data(self, text, entities):
        nar_entities = []
        # Iterate through each entity and find its position in the text
        for entity in entities:
            entity_text = entity["entity"]
            start_pos = text.find(entity_text)
            if start_pos != -1:
                end_pos = start_pos + len(entity_text)
                nar_entities.append((start_pos, end_pos, entity['label']))
            else:
                nar_entities.append((start_pos, end_pos, entity['label']))
        return nar_entities

# class NERGen:
#     @staticmethod
#     def get_ner_data(json_data):
#         corpus = ExtractionCorpus()
#         for item in json_data['ner']:
#             text = item['text']
#             ner_map = item['ner_map']
#             entity_list = []
#             for key, value in ner_map.items():
#                 entity_list.append(Entity(value, key))
#
#             corpus.add(CorpusData(text, entity_list))
#         return corpus.get()

# corpus = ExtractionCorpus()
# corpus.add(CorpusData("Please book a flight from New York to London on October 30 2024 at 10:00 AM.", [
#     Entity("flight", "FLIGHT"), Entity("New York", "SOURCE"), Entity("London", "DESTINATION"),
#     Entity("October 30 2024", "DATE"), Entity("10:00 AM", "TIME")
# ]))
# corpus.add(CorpusData("Please book a flight from Joypurhat to USA on 11/15/24 at 8:00 PM.", [
#     Entity("flight", "FLIGHT"), Entity("Joypurhat", "SOURCE"), Entity("USA", "DESTINATION"),
#     Entity("11/15/24", "DATE"), Entity("8:00 PM", "TIME")
# ]))
# corpus.add(CorpusData("Can you book a flight from Los Angeles to Paris on November 15 at 8:30 PM?", [
#     Entity("flight", "FLIGHT"), Entity("Los Angeles", "SOURCE"), Entity("Paris", "DESTINATION"),
#     Entity("November 15", "DATE"), Entity("8:30 PM", "TIME")
# ]))
# result = corpus.get()
# return result
