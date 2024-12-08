from enum import Enum


class LearningType(Enum):
    Supervised = 0
    Unsupervised = 1
    Semi_Supervised = 2
    Reinforcement = 3


class Algorithm(Enum):
    Liner_Regression = 0


class NN(Enum):
    FFN = 0


class Intelligence(Enum):
    Understanding_Interaction = 0
    Knowledge_Discovery = 1
    Decision_Making = 2
    Generation = 3


class CognitiveSkills(Enum):
    Information_Extraction = 0
    Clustering = 1
    Classification = 2
    Conversation_and_Dialogue_Systems = 3
    Regression = 4
    Anomaly_Detection = 5
    Recommendation_Systems = 6
    Dimensionality_Reduction = 7
    Natural_Language_Processing = 8
    Speech_Recognition_and_Synthesis = 9
    Object_Detection_and_Image_Recognition = 10
    Generative_Models = 11
    Reinforcement_Learning = 12
    Time_Series_Forecasting = 13
    Transfer_Learning = 14
    Data_Generation_and_Augmentation = 15
    Conversational_Intelligence = 16


class Meta:
    def __init__(self, learning_type, algorithm, NN, intelligence, cognitive_skills):
        self.LearningType: learning_type
        self.Algorithm: algorithm
        self.NN: NN
        self.Intelligence: intelligence
        self.CognitiveSkills: cognitive_skills
