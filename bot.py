import ai21


def dedent(text: str):
    return '\n'.join([m.lstrip() for m in text.split('\n')]).strip()


def prompt_template(**deco_kwargs):
    def real_decorator(func):

        def wrapper(*args, **func_kwargs):
            result = func(*args, **func_kwargs)
            if "dedent" in deco_kwargs and deco_kwargs["dedent"]:
                result = dedent(result)
            if "fix_whitespace" in deco_kwargs and deco_kwargs["fix_whitespace"]:
                result = result.strip()
            return result

        return wrapper

    return real_decorator


class Bot:

    def __init__(self):
        pass

    def generate_response(self, conversation_history: list) -> str:
        conversation_history_str = "\n".join(conversation_history)
        preset, request = get_commands(conversation_history_str)
        
        response = generate_text(request, preset)
        return response


@prompt_template(dedent=True, fix_whitespace=True)
def construct_get_commands_prompt(conversation: str):
    prompt = f"""
    Using the conversation as context, look at the most RECENT request and:
     - classify it to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
     - summarize the request in simpler terms

    User: Who is Canada's favorite figure skating pair?
    AI21 Discord Bot: The most popular pairs figure skaters in Canada are Tessa Virtue and Scott Moir, and Meagan Duhamel and Eric Radford.
    User: When did they win the Olympics?
    
    NLP Task: Question answering
    Request: When did Tessa Virtue and Scott Moir, and Meagan Duhamel and Eric Radford win the Olympics?
    ##
    Using the conversation as context, look at the most RECENT request and:
     - classify it to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
     - summarize the request in simpler terms
     
    User: Write me a love poem

    NLP Task: Long form generation
    Request: Write a love poem
    ##
    Using the conversation as context, look at the most RECENT request and:
     - classify it to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
     - summarize the request in simpler terms
     
    User: Describe what Africa is like to visit
    AI21 Discord Bot: Africa is a large and diverse continent, with a wide range of cultures and landscapes. Some popular destinations in Africa include Egypt, South Africa, and Kenya. These countries are known for their ancient civilizations, vibrant cities, and stunning natural beauty. Africa is also home to a number of national parks and reserves, including the Sahara Desert, the Serengeti, and the Ngorongoro Crater. These areas offer visitors the opportunity to experience Africa's rich wildlife and unique ecosystems. Overall, Africa is a fascinating place to visit, and it offers visitors a unique and unforgettable experience.
    User: Can you write a shorter description of that and focus on the culture?
    
    NLP Task: Paraphrasing
    Request: Write a shorter description of what Africa is like to visit and focus on the culture
    ##
    Using the conversation as context, look at the most RECENT request and:
     - classify it to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
     - summarize the request in simpler terms
    
    {conversation}
    
    NLP Task:"""
    return prompt


def get_commands(conversation_history_str: str):
    prompt = construct_get_commands_prompt(conversation_history_str)
    text = generate_text(prompt, "Classify NLP task")
    preset, request = text.split("Request:")
    return  preset.strip(), request[9:].strip()



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


def generate_text(prompt, preset):
    params = get_default_preset_params()
    preset_params = get_params_from_preset(preset)
    params.update(preset_params)
    #print("-----PARAMS---------")
    #print(params)
    #print("-----PROMPT---------")
    #print(prompt)
    response = ai21.Completion.execute(prompt=prompt, **params)
    #print("-----RESPONSE---------")
    #print(response["completions"][0]['data']['text'].strip())
    return response["completions"][0]['data']['text'].strip()
