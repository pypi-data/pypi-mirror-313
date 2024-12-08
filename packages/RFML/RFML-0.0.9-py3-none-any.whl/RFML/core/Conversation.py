import datetime


class Context:
    def __init__(self, model: str, label: str):
        self.model = model
        self.label = label

    def to_json(self):
        return {
            "model": self.model,
            "label": self.label,
        }


class Dialogs:
    you: str
    bot: str
    timeline: datetime

    def __init__(self, timeline: datetime, you: str, bot: str):
        self.timeline = timeline
        self.you = you
        self.bot = bot

    def to_json(self):
        return {
            "timeline": self.timeline,
            "you": self.you,
            "bot": self.bot
        }


class Conversation:
    def __init__(
            self, session_id, user_id, date, time, last_access,
            dialogs=None, context=None, prompt_cash=None
    ):
        if context is None: context = {}
        if dialogs is None: dialogs = []
        if prompt_cash is None: prompt_cash = {}
        self.session_id = session_id
        self.user_id = user_id
        self.date = date
        self.time = time
        self.last_access = last_access
        self.dialogs = dialogs
        self.context = context
        self.prompt_cash = prompt_cash

    def to_json(self):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "date": self.date,
            "time": self.time,
            "last_access": self.time,
        }
