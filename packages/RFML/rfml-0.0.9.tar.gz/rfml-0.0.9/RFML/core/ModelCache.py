class ModelCache:
    loaded_models = {}

    def load(self, model_name, model):
        self.loaded_models[model_name] = model

    def get(self, model_name):
        try:
            return self.loaded_models[model_name]
        except KeyError as ke:
            return None
