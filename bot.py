import csv
import os
from collections import Counter

import ai21
from simplechain.stack import TextEmbedderFactory, VectorDatabaseFactory


def dedent_text(text: str):
    return '\n'.join([m.lstrip() for m in text.split('\n')]).strip()


def prompt_template(dedent=True, fix_whitespace=True):
    def real_decorator(func):
        def wrapper(*args, **func_kwargs):
            result = func(*args, **func_kwargs)
            if dedent:
                result = dedent_text(result)
            if fix_whitespace:
                result = result.strip()
            return result
        return wrapper
    return real_decorator


class Bot:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        ai21.api_key = os.environ['AI21_API_KEY']
        self.embedder = TextEmbedderFactory.create("ai21")
        self.index = VectorDatabaseFactory.create("annoy", 768, "index.ann", "metadata.json")

    def setup_index(self):
        metadata = []
        paragraphs = []

        for row in csv.reader(open('data/AI21.csv', 'r', encoding='iso-8859-1')):
            metadata.append(row)
            paragraphs.append(row[0])

        # Breaks the strings with 2000+ characters into smaller strings
        for i, s in enumerate(paragraphs):
            if len(s) > 2000:
                paragraphs.pop(i)
                for j in range(0, len(s), 2000):
                    paragraphs.insert(i + j, s[j:j + 2000])

        embeds = self.embedder.embed_all(paragraphs)
        self.index.add_all(embeds, metadata)
        self.index.save()

    def generate_response(self, conversation_history: list, verbose: bool = False) -> str:
        conversation_history_str = "\n".join(conversation_history)
        preset, request, requires_ai21_index = get_commands(conversation_history_str)
        print("REQUIRES:", requires_ai21_index)
        context_str, links_str = "", ""
        if requires_ai21_index:
            context = self.index.get_nearest_neighbors(self.embedder.embed(request), 10)
            links_counter = Counter()
            for c in context:
                if float(c[1]) > 1.0:
                    continue
                links_counter[c[0][1]] += 1
                context_str += f"{c[0][0]}."
            links_str = "The following links may be useful:\n" + "\n".join([link[0] for link in links_counter.most_common(3)])

        prompt = construct_get_response_prompt(request, context_str)

        response = generate_text(prompt, preset, verbose) + links_str
        return response


@prompt_template(dedent=True, fix_whitespace=True)
def construct_get_commands_prompt(conversation: str):
    prompt = f"""
    Using the conversation as context, look at the most RECENT request and fill in the following:
    NLP Task: classify it to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
    Request: summarize the request in simpler terms
    Requires AI21 API: determine if the request requires information available on AI21 labs website as True/False

    User: Who is Canada's favorite figure skating pair?
    AI21 Discord Bot: The most popular pairs figure skaters in Canada are Tessa Virtue and Scott Moir, and Meagan Duhamel and Eric Radford.
    User: When did they win the Olympics?
    
    NLP Task: Question answering
    Request: When did Tessa Virtue and Scott Moir, and Meagan Duhamel and Eric Radford win the Olympics?
    Requires AI21 API: False
    ##
    Using the conversation as context, look at the most RECENT request and fill in the following:
    NLP Task: classify it to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
    Request: summarize the request in simpler terms
    Requires AI21 API: determine if the request requires information available on AI21 labs website as True/False

    User: Write me a love poem

    NLP Task: Long form generation
    Request: Write a love poem
    Requires AI21 API: False
    ##
    Using the conversation as context, look at the most RECENT request and:
    NLP Task: classify it to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
    Request: summarize the request in simpler terms
    Requires AI21 API: determine if the request requires information available on AI21 labs website as True/False

    User: Describe what Africa is like to visit
    AI21 Discord Bot: Africa is a large and diverse continent, with a wide range of cultures and landscapes. Some popular destinations in Africa include Egypt, South Africa, and Kenya. These countries are known for their ancient civilizations, vibrant cities, and stunning natural beauty. Africa is also home to a number of national parks and reserves, including the Sahara Desert, the Serengeti, and the Ngorongoro Crater. These areas offer visitors the opportunity to experience Africa's rich wildlife and unique ecosystems. Overall, Africa is a fascinating place to visit, and it offers visitors a unique and unforgettable experience.
    User: Can you write a shorter description of that and focus on the culture?
    
    NLP Task: Paraphrasing
    Request: Write a shorter description of what Africa is like to visit and focus on the culture
    Requires AI21 API: False
    ##
    Using the conversation as context, look at the most RECENT request and:
    NLP Task: classify it to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
    Request: summarize the request in simpler terms
    Requires AI21 API: determine if the request requires information available on AI21 labs website as True/False

    {conversation}
    
    NLP Task:"""
    return prompt


def get_commands(conversation_history_str: str):
    prompt = construct_get_commands_prompt(conversation_history_str)
    text = generate_text(prompt, "Classify NLP task", verbose=False)
    preset, request, requires_ai21_index = text.split("\n")
    return preset.strip(), request[9:].strip(), requires_ai21_index[19:].strip() == "True"


def get_params_from_preset(preset: str) -> dict:
    # TODO Check presence penalties
    if preset == "Classify NLP task":
        return {
            "model": "j2-jumbo-instruct",
            "maxTokens": 100,
            "temperature": 0,
            "topP": 1,
            "stopSequences": ["##"]
        }

    if preset == "Generate code":
        return {
            "model": "j2-grande-instruct",
            "maxTokens": 100,
            "temperature": 0,
            "topP": 1,
        }

    if preset == "Paraphrasing":
        return {
            "model": "j2-jumbo",
            "maxTokens": 100,
            "temperature": 0.3,
            "topP": 1,
        }

    if preset == "Long form generation":
        return {
            "model": "j2-jumbo-instruct",
            "maxTokens": 300,
            "temperature": 0.84,
            "topP": 1
        }

    if preset == "Question answering":
        return {
            "model": "j2-jumbo-instruct",
            "maxTokens": 70,
            "temperature": 0.8,
            "topP": 1,
        }

    # use default preset params
    return {}


def get_default_preset_params():
    return {
        "model": "j2-grande-instruct",
        "maxTokens": 100,
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


@prompt_template(dedent=True, fix_whitespace=True)
def construct_get_response_prompt(request: str, context: str) -> str:
    if not context:
        return request

    return f"""Context: {context}
    Question: {request}"""


def generate_text(prompt, preset, verbose):
    params = get_default_preset_params()
    preset_params = get_params_from_preset(preset)
    params.update(preset_params)

    response = ai21.Completion.execute(prompt=prompt, **params)
    #from pprint import pprint
    #pprint(response)
    response = response["completions"][0]['data']['text'].strip()
    response = format_response(response, preset, preset_params, verbose)

    return response


def format_response(response, preset, preset_params, verbose):
    if preset == "Generate code":
        response = f"```{response}```"

    if verbose:
        response += f"\n\n*The above text was generated using the following parameters:" \
                    f"\nPreset: {preset}" \
                    f"\nModel: {preset_params['model']}" \
                    f"\nTemperature: {preset_params['temperature']}" \
                    f"\ntopP: {preset_params['topP']}*"

    return response


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    bot = Bot()
    bot.setup_index()
