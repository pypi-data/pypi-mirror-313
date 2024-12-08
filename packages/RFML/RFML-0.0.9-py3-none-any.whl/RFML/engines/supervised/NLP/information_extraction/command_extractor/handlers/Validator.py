from RFML.core.Results import PromptProcessResult
from RFML.interface.IPromptValidator import IPromptValidator
from RFML.prompt.PromptCash import PromptCash
from RFML.prompt.PromptQuery import PromptQuery


class Validator(IPromptValidator):
    # configure prompt_queries for validation check
    def configure_prompt_queries(self, model_name: str, prompt_query_list: list[PromptQuery]):
        if model_name == "rf-ce-flight_booking":
            self.flight_validation(prompt_query_list)
        elif model_name == "rf-ce-pr_process":
            self.pr_validation(prompt_query_list)

    def pr_validation(self, prompt_query_list: list[PromptQuery]):
        prompt_query_list.append(
            PromptQuery("Action", {
                "Q1": "Could you specify PR action type?",
                "Q2": "Please specify the PR action"
            })
        )
        # show
        prompt_query_list.append(
            PromptQuery("Time", {
                "Q1": "Could you specify the time?",
                "Q2": "Please mention time."
            })
        )
        # approve
        prompt_query_list.append(
            PromptQuery("PR", {
                "Q1": "Could you specify the PR no?",
                "Q2": "Please mention PR no."
            })
        )

    def flight_validation(self, prompt_query_list: list[PromptQuery]):
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
                "Q1": "Could you specify the journey time...?",
                "Q2": "Please mention the the journey time..."
            })
        )

    # process input and store in prompt_queries for validation check
    def process_prompt_queries(self, model_name: str, pc: PromptCash, user_input: str) -> PromptProcessResult:
        if model_name == "rf-ce-pr_process":
            if pc.missing_validator_attribute == "Time" and user_input != "today":
                return PromptProcessResult(False, "Please provide only (today) as date")
        # if pc: pc.validator_cash[pc.missing_validator_attribute] = user_input

    def format_prompt_queries(self, model_name: str, pc: PromptCash, valid_fields, user_input: str):
        import re
        if model_name == "rf-ce-flight_booking":
            msg = ""
            if valid_fields.get('Origin'): msg += f"Please book a flight from {valid_fields['Origin']} to "
            if valid_fields.get('Destination'): msg += f"{valid_fields['Destination']} on "
            if valid_fields.get('Date'): msg += f"{valid_fields['Date']} at "
            if valid_fields.get('Time'): msg += f"{valid_fields['Time']}."
            result = re.sub(r"\b(at|on|to)\b$", "", msg.strip()).strip()
            return result
        elif model_name == "rf-ce-pr_process":
            msg = ""
            if valid_fields.get('Action') == "show":
                if valid_fields.get('Time'): msg = f"show me PRs to approve {valid_fields['Time']}"
            elif valid_fields.get('Action') == "approve":
                if valid_fields.get('PR'): msg = f"please approve the PR number {valid_fields['PR']}"
            elif valid_fields.get('Action') == "disapprove":
                if valid_fields.get('PR'): msg = f"Please disapprove PR number {valid_fields['PR']}"
            return msg
