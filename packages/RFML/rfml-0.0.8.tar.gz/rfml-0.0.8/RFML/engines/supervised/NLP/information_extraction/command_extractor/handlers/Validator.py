from RFML.interface.IPromptValidator import IPromptValidator
from RFML.prompt.PromptCash import PromptCash
from RFML.prompt.PromptQuery import PromptQuery


class Validator(IPromptValidator):
    # configure prompt_queries for validation check
    def configure_prompt_queries(self, prompt_query_list: list[PromptQuery]):
        prompt_query_list.append(
            PromptQuery("Action", {
                "Q1": "Could you specify the transport type?",
                "Q2": "Please specify the transport"
            })
        )
        prompt_query_list.append(
            PromptQuery("Origin", {
                "Q1": "Could you specify the source location?",
                "Q2": "Please mention source location."
            })
        )
        prompt_query_list.append(
            PromptQuery("Destination", {
                "Q1": "Could you specify the destination location?",
                "Q2": "Please mention destination location."
            })
        )
        prompt_query_list.append(
            PromptQuery("Date", {
                "Q1": "Could you specify the journey date?",
                "Q2": "Please mention the the journey date."
            })
        )
        prompt_query_list.append(
            PromptQuery("Time", {
                "Q1": "Could you specify the journey time?",
                "Q2": "Please mention the the journey time."
            })
        )

    # process input and store in prompt_queries for validation check
    def process_prompt_queries(self, pc: PromptCash, user_input: str):
        if pc: pc.validator_cash[pc.missing_validator_attribute] = user_input

    def format_prompt_queries(self, pc: PromptCash, valid_fields, user_input: str):
        import re
        msg = ""
        if valid_fields.get('Origin'): msg += f"Please book a flight from {valid_fields['Origin']} to "
        if valid_fields.get('Destination'): msg += f"{valid_fields['Destination']} on "
        if valid_fields.get('Date'): msg += f"{valid_fields['Date']} at "
        if valid_fields.get('Time'): msg += f"{valid_fields['Time']}."
        result = re.sub(r"\b(at|on|to)\b$", "", msg.strip()).strip()
        return result
