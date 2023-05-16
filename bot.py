import csv
import os

import ai21

from index import Indexer
from prompts import construct_get_response_prompt, construct_get_commands_prompt


class Bot:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        ai21.api_key = os.environ['AI21_API_KEY']
        self.indexer = Indexer()

    def generate_response(self, conversation_history: list, verbose: bool = False) -> tuple:
        conversation_history_str = "\n".join(conversation_history)
        preset, request, requires_ai21_index = get_commands(conversation_history_str)

        context_str, links_str = "", ""
        if requires_ai21_index:
            context_str, links_str = self.indexer.get_context(request, n=100)

        prompt = construct_get_response_prompt(request, context_str, conversation_history_str)

        response, verbose_str = generate_text(prompt, preset, verbose)
        if response.startswith("AI21 Discord ChatBot: "):
            response = response[21:]
        response += f"\n\n{links_str}"
        return response, verbose_str


def get_commands(conversation_history_str: str):
    prompt = construct_get_commands_prompt(conversation_history_str)
    text, _ = generate_text(prompt, "Classify NLP task")
    preset, request, requires_ai21_index = text.split("\n")
    return preset.strip(), request[9:].strip(), requires_ai21_index[19:].strip() == "True"


def get_params_from_preset(preset: str) -> dict:
    if preset == "Classify NLP task":
        return {
            "model": "j2-jumbo-instruct",
            "maxTokens": 512,
            "temperature": 0,
            "topP": 1,
            "stopSequences": ["##"]
        }

    if preset == "Generate code":
        return {
            "model": "j2-grande-instruct",
            "maxTokens": 512,
            "temperature": 0,
            "topP": 1,
        }

    if preset == "Paraphrasing":
        return  {
            "model": "j2-jumbo-instruct",
            "maxTokens": 512,
            "temperature": 0.3,
            "topP": 1,
        }
    
    if preset == "Long form generation":
        return  {
            "model": "j2-jumbo-instruct",
            "maxTokens": 512,
            "temperature": 0.84,
            "topP": 1,
            "numResults": 1,
        }

    if preset == "Question answering":
        return {
            "model": "j2-jumbo-instruct",
            "maxTokens": 512,
            "temperature": 0.8,
            "topP": 1,
        }

    # use default preset params
    return {}


def get_default_preset_params():
    return {
        "model": "j2-grande-instruct",
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

    if preset == "Question answering" and context!="":
        response = ai21.Experimantal.Answer.execute(context=prompt, question=prompt)
        if verbose:
            verbose_str = f"\n\n:information_source: **The above text was generated using the Contextual Question Answering service by provided by AI21 Labs.**" \
                        f"\nSee more at https://docs.ai21.com/docs/contextual-answers-api"
    else: # foundation models
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