# from RFML.interface.ICognitive import ICognitive


class CognitiveModule:
    model_name: str
    engine: any
    default: False

    def __init__(self, engine: any, default: bool = False):
        from RFML.core.Cognitive import Cognitive
        _engine: Cognitive = engine
        self.model_name = _engine.model
        self.engine = engine
        self.default = default
