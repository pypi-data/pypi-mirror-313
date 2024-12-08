from enum import Enum
from RFML.core.Hosts import HTTPHost, CLIHost, TelegramHost
from RFML.interface.IPrompt import IPrompt


class Interface(Enum):
    CLI = 1
    API = 2
    PubSub = 3
    Telegram = 4
    WhatsApp = 5
    Facebook = 6


class Prompt:
    interface = Interface.CLI
    handler = any
    cancel_request = True
    pass_request_length = 15

    def __init__(self, interface: Interface, handler: IPrompt = None, cancel_request=True, pass_request_length=15):
        self.interface = interface
        self.handler = handler
        self.cancel_request = cancel_request
        self.pass_request_length = pass_request_length

    def invoke_prompt(self, lib_core_process_callback):
        if self.interface == Interface.API:
            print("API Host has been attached")
            HTTPHost(
                self.handler,  # client handler
                lib_core_process_callback,  # FW callback
                self.cancel_request,
                self.pass_request_length
            )
        elif self.interface == Interface.CLI:
            print("Wellcome to OnDesk Bot")
            CLIHost(
                self.handler, lib_core_process_callback,
                self.cancel_request,
                self.pass_request_length
            )
        elif self.interface == Interface.Telegram:
            print("Wellcome to OnDesk Bot")
            TelegramHost(
                self.handler, lib_core_process_callback,
                self.cancel_request,
                self.pass_request_length
            )
