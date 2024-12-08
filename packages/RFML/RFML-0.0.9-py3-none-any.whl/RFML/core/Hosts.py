import re
from flask import *
from RFML.core.Interaction import Interaction, TaskType
from RFML.interface.IPrompt import IPrompt
import telebot


class HTTPHost:
    def __init__(self, prompt: IPrompt, request_process_callback, cancel_request=True, pass_request_length=15):
        app = Flask(__name__)

        @app.route("/interact/", methods=['POST'])
        def interact():
            session_id = request.headers.get("X-Session-ID")

            model = request.json['model']
            task = request.json['task']
            user_input = request.json['input']

            interaction = Interaction(
                session_id=session_id,
                model=model,
                task=TaskType(task),
                user_input=user_input,
                cancel_request=cancel_request,
                pass_request_length=pass_request_length
            )

            prompt_in_input = prompt.on_prompt_in(interaction.input)
            interaction.input = prompt_in_input or interaction.input
            result = request_process_callback(interaction)
            # prompt_in_output = prompt.on_prompt_out(result)

            return result  # in JSON format

        #   if __name__ == "__main__":
        app.run()

        print("HTTP Host is up and running")


class CLIHost:
    session_id = ""

    def __init__(self, prompt: IPrompt, lib_core_process_callback, cancel_request=True, pass_request_length=15):
        print("Let's chat! (type 'quit' to exit)")
        while True:
            sentence = input("You: ")  # sentence = "do you use credit cards?"
            if sentence == "quit": break

            cmd = re.search(r"rf\s(train|gen|reload|reg)(?:\s(\S+))?", sentence)
            tasks = {
                "train": TaskType.Train, "gen": TaskType.Generate, "reload": TaskType.Reload, "reg": TaskType.Register
            }

            cmd_set_session = False
            if cmd:
                if cmd.group(1) == "reg":
                    cmd_set_session = True
                    self.session_id = cmd.group(2)

            interaction = Interaction(
                session_id=self.session_id,
                model=cmd.group(2) if cmd else "",
                task=tasks.get(cmd.group(1) if cmd else "", TaskType.Predict),
                user_input=sentence,
                cancel_request=cancel_request,
                pass_request_length=pass_request_length
            )

            if prompt:
                prompt_in_input = prompt.on_prompt_in(interaction.input)
                interaction.input = prompt_in_input or interaction.input
                if not cmd_set_session:
                    result = lib_core_process_callback(interaction)
                    prompt.on_prompt_out(result)
                else:
                    prompt.on_prompt_out(f"Session id # {cmd.group(2)} is registered!")
            else:
                result = lib_core_process_callback(interaction)
                print(result)


class TelegramHost:
    session_id = ""

    def __init__(self, prompt: IPrompt, lib_core_process_callback, cancel_request=True, pass_request_length=15):
        # Replace ‘YOUR_API_TOKEN’ with the API token you received from the BotFather
        API_TOKEN = '7084272751:AAH70cW_72DjmSGSr_J3J8qj1xxgya24PIo'

        bot = telebot.TeleBot(API_TOKEN)

        # Define a command handler
        @bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            bot.reply_to(message, 'Welcome to YourBot! Type /info to get more information.')

        @bot.message_handler(commands=['info'])
        def send_info(message):
            bot.reply_to(message, 'This is a simple Telegram bot implemented in Python.')

        # Define a message handler
        @bot.message_handler(func=lambda message: True)
        def echo_all(message):
            result = self.predict_bot(
                prompt=prompt, session_id=self.session_id, sentence=message.text,
                pass_request_length=pass_request_length, cancel_request=cancel_request,
                lib_core_process_callback=lib_core_process_callback
            )
            bot.reply_to(message, result['msg'])

        # Start the bot
        bot.polling()

    def predict_bot(
            self, prompt: IPrompt, session_id, sentence, cancel_request, pass_request_length,
            lib_core_process_callback
    ):
        interaction = Interaction(
            session_id=session_id,
            model="",
            task=TaskType.Predict,
            user_input=sentence,
            cancel_request=cancel_request,
            pass_request_length=pass_request_length
        )

        if prompt:
            prompt_in_input = prompt.on_prompt_in(interaction.input)
            interaction.input = prompt_in_input or interaction.input
            result = lib_core_process_callback(interaction)
            prompt.on_prompt_out(result)
            return result
        else:
            result = lib_core_process_callback(interaction)
            print(result)
            return result
