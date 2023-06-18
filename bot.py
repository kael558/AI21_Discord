import os

import ai21

from index import Indexer
from prompts import construct_get_response_prompt, construct_get_commands_prompt
import requests
import json


class Bot:
    def __init__(self, name="AI21 Discord ChatBot", logger=None):
        from dotenv import load_dotenv
        load_dotenv()
        ai21.api_key = os.environ['AI21_API_KEY']
        self.indexer = Indexer()
        self.logger = logger
        self.name = name

    async def generate_response(self, conversation_history: list, verbose: bool = False, users=None) -> tuple:
        if users is None:
            users = []
        conversation_history_str = "\n".join(conversation_history)
        preset, request, ai21_webpage_title = await get_commands(conversation_history_str)
        if request == "None":  # If no request was given, use the last user input
            user_input = conversation_history[-1].split(':', 1)
            request = user_input[1].strip()

        context_str, links_str = "", ""
        if ai21_webpage_title:
            try:
                context_str, links_str = self.indexer.get_context(ai21_webpage_title, n=3)
            except Exception as e:
                if self.logger:
                    self.logger.error(e)
                context_str, links_str = "", ""

        if context_str:
            prompt = request
        else:
            prompt = construct_get_response_prompt(self.name, request, conversation_history_str, ", ".join(users))

        response, verbose_str = generate_text(prompt, preset, context_str, verbose)
        if response.startswith("AI21 Discord ChatBot: "):
            response = response[21:]
        if links_str:
            response += f"\n\n{links_str}"
        return response.strip(), verbose_str.strip()


async def get_commands(conversation_history_str: str):
    prompt = construct_get_commands_prompt(conversation_history_str)
    text, _ = await generate_text(prompt, "Classify NLP task")
    lines = text.split("\n")

    ai21_webpage_title = "None"

    if len(lines) == 2:
        preset, request = lines
    elif len(lines) == 3:
        preset, request, ai21_webpage_title = text.split("\n")
        ai21_webpage_title = ai21_webpage_title[20:].strip()
    else:
        preset = "Default"
        request = "None"

    if ai21_webpage_title == "None":
        ai21_webpage_title = None

    return preset.strip(), request[9:].strip(), ai21_webpage_title


def get_params_from_preset(preset: str) -> dict:
    if preset == "Classify NLP task":
        return {
            "model": "j2-ultra",
            "maxTokens": 512,
            "temperature": 0,
            "topP": 1,
            "stopSequences": ["##"]
        }

    if preset == "Generate code":
        return {
            "model": "j2-mid",
            "maxTokens": 512,
            "temperature": 0,
            "topP": 1,
        }

    if preset == "Paraphrasing":
        return {
            "model": "j2-ultra",
            "maxTokens": 512,
            "temperature": 0.3,
            "topP": 1,
        }

    if preset == "Long form generation":
        return {
            "model": "j2-ultra",
            "maxTokens": 512,
            "temperature": 0.84,
            "topP": 1,
            "numResults": 1,
        }

    if preset == "Question answering":
        return {
            "model": "j2-ultra",
            "maxTokens": 512,
            "temperature": 0.8,
            "topP": 1,
        }

    # use default preset params
    return {}


def get_default_preset_params():
    return {
        "model": "j2-mid",
        "maxTokens": 512,
        "temperature": 0.7,
        "topP": 1,
        "topKReturn": 0,
        "numResults": 1,
        "countPenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        "frequencyPenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        "presencePenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        }
    }


def generate_text(prompt, preset, context="", verbose=False):
    verbose_str = ""

    if preset == "Question answering" and context and context != "":
        url = "https://api.ai21.com/studio/v1/experimental/answer"
        payload = {
            "context": context,
            "question": prompt
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {os.environ['AI21_API_KEY']}"
        }
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            response = "I couldn't find the answer to your question."
        else:
            response = response.json()
            if "answer" not in response or response["answer"] == "Answer not in document":
                response = "I couldn't find the answer to your question."
            else:
                response = response["answer"]

        # response = ai21.Experimantal.Answer.execute(context=context, question=prompt)
        if verbose:
            verbose_str = f"\n\n:information_source: **The above text was generated using the Contextual Question Answering API provided by AI21 Labs.**" \
                          f"\nSee more at https://docs.ai21.com/docs/contextual-answers-api"
    else:  # foundation models
        params = get_default_preset_params()
        preset_params = get_params_from_preset(preset)
        params.update(preset_params)
        response = ai21.Completion.execute(prompt=prompt, **params)["completions"][0]["data"]["text"].strip()
        if verbose:
            verbose_str = f"\n\n:information_source: **The above text was generated using the following:**" \
                          f"\nPreset: *{preset}*" \
                          f"\nModel: *{preset_params['model']}*" \
                          f"\nTemperature: *{preset_params['temperature']}*" \
                          f"\ntopP: *{preset_params['topP']}*" \
                          f"\n**---Prompt---**\n>>> {prompt}"

    if preset == "Generate code":
        response = f"```{response}```"

    return response.strip(), verbose_str.strip()
