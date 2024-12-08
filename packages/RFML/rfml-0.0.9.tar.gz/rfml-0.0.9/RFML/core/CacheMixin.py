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
        is_canceled = rf.nlp.prompt.is_cancel_text(interaction.input)
        if interaction.cancel_request and is_canceled: pc.set_cancel_prompt()
        if 0 < interaction.pass_request_length < len(interaction.input): pc.set_pass_prompt()
        if pc: pc.validator_cash[pc.missing_validator_attribute] = interaction.input # collect prompt input
        process_result = cognitive.handlers.validator.process_prompt_queries(cognitive.model, pc, interaction.input)
        if not is_canceled:
            if process_result:
                if not process_result.valid:
                    return PredictResult(
                        session_id=interaction.session_id,
                        label=predict_result.label,
                        message=process_result.message,  # "not valid input message"
                    )

        cognitive.corpus.prompt_cash.update(interaction.session_id, pc.to_json())  # how to avoide?

        all_required_fields = PromptQuery.get_validation_attributes(prompt_queries)  # {"room":"joba", "a":"b"}

        # remove key from validation based on validator_cash
        required_fields = {
            key: pc.validator_cash[key] for key in pc.validator_cash if key in all_required_fields
        }
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
