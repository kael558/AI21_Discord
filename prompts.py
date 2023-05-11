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

@prompt_template(dedent=True, fix_whitespace=True)
def construct_get_commands_prompt(conversation: str):
    prompt = f"""
    Using the conversation as context, look at the most RECENT request and fill in the following:
    NLP Task: classify it to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
    Request: summarize the request in simpler terms
    Requires AI21 API: determine if the request requires information available on AI21 labs website as True/False

    User: Who is Canada's favorite figure skating pair?
    AI21 Discord ChatBot: The most popular pairs figure skaters in Canada are Tessa Virtue and Scott Moir, and Meagan Duhamel and Eric Radford.
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
    AI21 Discord ChatBot: Africa is a large and diverse continent, with a wide range of cultures and landscapes. Some popular destinations in Africa include Egypt, South Africa, and Kenya. These countries are known for their ancient civilizations, vibrant cities, and stunning natural beauty. Africa is also home to a number of national parks and reserves, including the Sahara Desert, the Serengeti, and the Ngorongoro Crater. These areas offer visitors the opportunity to experience Africa's rich wildlife and unique ecosystems. Overall, Africa is a fascinating place to visit, and it offers visitors a unique and unforgettable experience.
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


@prompt_template(dedent=True, fix_whitespace=True)
def construct_get_response_prompt(request: str, context: str, conversation: str) -> str:
    prompt = """Welcome! I am AI21 Discord ChatBot. I'm here to answer your questions, provide advice, or just have a friendly conversation.
    Please note that while I can provide general information and guidance, I am not a licensed professional and my responses are not intended to be a substitute for professional advice. 
    Additionally, I strive to remain neutral and respectful in all interactions, and I do not engage in discriminatory or harmful behavior. 
    """

    if context:
        prompt += f"I am given the following information: {context}\n"

    prompt += f"""
    I will use the following conversation between me (AI21 Discord ChatBot) and a User as context:
    {conversation}

    It seems like the User is asking me for this: {request}

    Write a response to their question or instruction."""
    return prompt


