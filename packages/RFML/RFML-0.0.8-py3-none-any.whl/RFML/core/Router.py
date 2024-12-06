from RFML.core.Results import PredictResult


class Router:
    @staticmethod
    def redirect(cognitive, prompt_queries, before_predict_text) -> PredictResult:
        if cognitive.handlers.validator:
            cognitive.handlers.validator.configure_prompt_queries(prompt_queries)
        predict_result = cognitive.handlers.predictor.predict(cognitive.model, before_predict_text,
                                                              cognitive.corpus)
        return predict_result
