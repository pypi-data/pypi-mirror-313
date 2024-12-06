import datetime

from RFML.core.Cognitive import Cognitive
from RFML.core.Conversation import Conversation, Context, Dialogs
from RFML.core.Interaction import Interaction
from RFML.core.Results import PredictResult, ResultType
from RFML.libs.utils import rf
from RFML.prompt.PromptCash import PromptCash
from RFML.prompt.PromptQuery import PromptQuery


class CacheMixin:  # partial class for Conversation and PromptQuery cache
    @staticmethod
    def log_conversation(interaction: Interaction, cognitive: Cognitive):
        conversation = cognitive.corpus.conversation.read({"session_id": interaction.session_id})
        if conversation:
            conversation.last_access = datetime.datetime.now()
            cognitive.corpus.conversation.update(interaction.session_id, conversation.to_json())
        else:
            _conversation = Conversation(
                session_id=interaction.session_id,
                date=datetime.datetime.now(),
                time=datetime.datetime.now(),
                user_id=cognitive.access_control.user_id,
                last_access=datetime.datetime.now(),
            )
            json = _conversation.to_json()
            json.update({"dialogs": [], "context": {}, "prompt_cash": {}})
            cognitive.corpus.conversation.save(json)
            conversation = _conversation

        return conversation

    @staticmethod
    def log_context(cognitive: Cognitive, interaction: Interaction, predict_result: PredictResult):
        # update conversation.context_cash (new label, new model)
        cognitive.corpus.context.update(
            interaction.session_id,
            Context(predict_result.model, predict_result.label).to_json()
        )

        # update dialogs
        cognitive.corpus.dialog.push(
            interaction.session_id,
            Dialogs(datetime.datetime.now(), interaction.input, predict_result.message).to_json()
        )

        # do_not_understand
        if predict_result.result_type == ResultType.do_not_understand:
            cognitive.corpus.do_not_understand.push(interaction.session_id, interaction.input)

    @staticmethod
    def process_prompt(
            pc: PromptCash, interaction: Interaction, cognitive: Cognitive, predict_result: PredictResult,
            prompt_queries: [PromptQuery]
    ):
        cancel_request = interaction.cancel_request
        pass_request_length = interaction.pass_request_length
        if cancel_request and rf.nlp.prompt.is_cancel_text(interaction.input): pc.cancel_prompt()
        if 0 < pass_request_length < len(interaction.input): pc.pass_prompt()
        pc.validator_cash[pc.missing_validator_attribute] = interaction.input
        cognitive.handlers.validator.process_prompt_queries(pc, interaction.input)

        cognitive.corpus.prompt_cash.update(interaction.session_id, pc.to_json())  # how to avoide?

        required_fields = PromptQuery.get_validation_attributes(prompt_queries)  # {"room":"joba", "a":"b"}
        last_key = list(required_fields.keys())[-1]
        for key, value in required_fields.items():

            if not pc.validator_cash[key]:  # not given or empty
                pc.missing_validator_attribute = key
                pc.last_prompt_query = PromptQuery.get_query_value(key, prompt_queries)
                pc.last_user_input = interaction.input
                cognitive.corpus.prompt_cash.update(interaction.session_id, pc.to_json())
                return PredictResult(
                    session_id=interaction.session_id,
                    label=predict_result.label,
                    probability=0.0,
                    message=PromptQuery.get_query_value(key, prompt_queries),  # "what is the room name?"
                    route=""
                )

        return None  # None will ensure predict call
