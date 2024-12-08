import json
from random import randrange

from RFML.core.Results import PredictResult, ResultType
from RFML.corpus.Corpus import Corpus
from RFML.prompt.PromptCash import PromptCash


class Mismatch:
    valid = False
    message = ""

    def __init__(self, valid: bool, message):
        self.valid = valid
        self.message = message


class PromptQuery:
    propriety = ""
    queries = {}
    value = str

    def __init__(self, propriety: str = "", queries=None, value: str = None):
        if queries is None:
            queries = {}
        self.propriety = propriety
        self.queries = queries
        self.value = value

    @staticmethod
    def get_query(attribute: str, prompt_queries: [], query_no: str = ""):
        query = any
        for item in prompt_queries:
            if item.propriety == attribute:
                query = item.queries
                break

        if not query_no:
            query_list = []
            for key, value in query.items(): query_list.append((key, value))
            rnd = randrange(len(query_list))  # pick random question
            q_no = query_list[rnd][0]
            q_text = query_list[rnd][1]
            return {q_no: q_text}
        else:
            return {query_no: query[query_no]}

    @staticmethod
    def get_query_value(attribute: str, prompt_queries: [], query_no: str = ""):
        # get_first_value = lambda json_obj: next(iter(json_obj.values()), None)
        val = next(iter(PromptQuery.get_query(attribute, prompt_queries, query_no).values()), None)
        return val

    @staticmethod
    def get_validation_attributes(prompt_queries: []):
        validation_attributes = {}  # {"room":"joba", "from":"1-1-1"}
        for item in prompt_queries:
            validation_attributes[item.propriety] = item.value
            # validation_attributes.update({item.propriety: item.value})
            # for key, value in item.queries.items(): print(f"{key},{value}")
        return validation_attributes

    @staticmethod
    def validate(session_id: str, predict_result: PredictResult, prompt_queries: [], corpus: Corpus) -> Mismatch:
        # compare predict_result with validator_cash and return True or False
        if predict_result.result_type == ResultType.do_not_understand: return Mismatch(valid=True, message="")  # no msg
        if not predict_result: return Mismatch(valid=True, message="")  # no msg
        all_required_fields = PromptQuery.get_validation_attributes(prompt_queries)  # {"room":"joba", "a":"b"}

        # remove key from validation based on model output
        required_fields = {
            key: predict_result.message[key] for key in predict_result.message if key in all_required_fields
        }
        for key in required_fields:

            # _datas = json.loads(json.dumps(predict_result.message)) # check key exists
            # for _data in _datas:
            #     if key not in _data: return Mismatch(valid=True, message=_datas)

            if predict_result.message[key] is None or predict_result.message[key] == "":  # if key value is empty
                _json = {
                    "validator_cash": predict_result.message,
                    "missing_validator_attribute": key,
                    "last_prompt_query": PromptQuery.get_query_value(key, prompt_queries),
                    "last_user_input": ""
                }
                if session_id:
                    pc: PromptCash = PromptCash(_json)
                    corpus.prompt_cash.update(session_id, pc.to_json())

                message = "Please provide required information "
                if not session_id:
                    for key1 in predict_result.message: message += f"{key1}, "
                    return Mismatch(valid=False, message=message[:-2])  # all info
                else:
                    return Mismatch(valid=False, message=PromptQuery.get_query_value(key, prompt_queries))  # only 1 Q

        return Mismatch(valid=True, message="")  # all info
