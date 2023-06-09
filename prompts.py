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
    Using the conversation as context, look at the LAST message and fill in the following:
    NLP Task: classify it to one of the following NLP tasks: Generating code, Paraphrasing, Long form generation, Question answering
    Request: summarize what the LAST user is asking in simple terms
    AI21 Webpage Title: if the request requires information available on AI21 labs website, what would be the title of the webpage? Else None
    
    ---CONVERSATION---
    User: Who is Canada's favorite figure skating pair?
    AI21 Discord ChatBot: The most popular pairs figure skaters in Canada are Tessa Virtue and Scott Moir, and Meagan Duhamel and Eric Radford.
    User: When did they win the Olympics?

    NLP Task: Question answering
    Request: When did Tessa Virtue and Scott Moir, and Meagan Duhamel and Eric Radford win the Olympics?
    AI21 Webpage Title: None
    ##
    Using the conversation as context, look at the LAST message and fill in the following:
    NLP Task: classify it to one of the following NLP tasks: Generating code, Paraphrasing, Long form generation, Question answering
    Request: summarize what the LAST user is asking in simple terms
    AI21 Webpage Title: if the request requires information available on AI21 labs website, what would be the title of the webpage? Else None

    ---CONVERSATION---
    User: What the price of the praphrasing api?

    NLP Task: Question answering
    Request: Paraphrasing api price
    AI21 Webpage Title: Pricing
    ##
    Using the conversation as context, look at the LAST message and fill in the following:
    NLP Task: classify it to one of the following NLP tasks: Generating code, Paraphrasing, Long form generation, Question answering
    Request: summarize what the LAST user is asking in simple terms
    AI21 Webpage Title: if the request requires information available on AI21 labs website, what would be the title of the webpage? Else None
    
    ---CONVERSATION---
    User: Describe what Africa is like to visit
    AI21 Discord ChatBot: Africa is a large and diverse continent, with a wide range of cultures and landscapes. Some popular destinations in Africa include Egypt, South Africa, and Kenya. These countries are known for their ancient civilizations, vibrant cities, and stunning natural beauty. Africa is also home to a number of national parks and reserves, including the Sahara Desert, the Serengeti, and the Ngorongoro Crater. These areas offer visitors the opportunity to experience Africa's rich wildlife and unique ecosystems. Overall, Africa is a fascinating place to visit, and it offers visitors a unique and unforgettable experience.
    User: Can you write a shorter description of that and focus on the culture?

    NLP Task: Paraphrasing
    Request: Write a shorter description of what Africa is like to visit and focus on the culture
    AI21 Webpage Title: None
    ##
    Using the conversation as context, look at the LAST message and fill in the following:
    NLP Task: classify it to one of the following NLP tasks: Generating code, Paraphrasing, Long form generation, Question answering
    Request: summarize what the LAST user is asking in simple terms
    AI21 Webpage Title: if the request requires information available on AI21 labs website, what would be the title of the webpage? Else None

    ---CONVERSATION---
    User: Do any of the J2 models support batch transform? Which?

    NLP Task: Question answering
    Request: J2 models batch transform
    AI21 Webpage Title: J2 models
    ##
    Using the conversation as context, look at the LAST message and fill in the following:
    NLP Task: classify it to one of the following NLP tasks: Generating code, Paraphrasing, Long form generation, Question answering
    Request: summarize what the LAST user is asking in simple terms
    AI21 Webpage Title: if the request requires information available on AI21 labs website, what would be the title of the webpage? Else None
    
    ---CONVERSATION---
    {conversation}

    NLP Task:"""
    return prompt


@prompt_template(dedent=True, fix_whitespace=True)
def construct_get_response_prompt(name: str, request: str,
                                  conversation: str) -> str:
    prompt = f"""My name is {name}. 
        I am a Discord Chatbot powered entirely by AI21's language models. I can see up to 3 messages in the past but I can only see messages with a question mark reaction.

        Please note that I am not a licensed professional and my responses are not intended to be a substitute for professional advice.  I may hallucinate or make mistakes, so please use your own judgment when making decisions based on my responses. 
        
        I will do any task that involves generating text. For example, I can answer questions, provide advice, or just have a friendly conversation. 
        I can also answer questions about AI21 Labs because I have special access to information available on their website.
        
        ---CONVERSATION---
        {conversation}
    """

    if request:
        prompt += f"""
        It seems like the users are asking me for this: "{request}"
        """

    prompt += f"""
        I am able to answer ANY request. My response to satisfy the user's request:
        {name}:"""

    return prompt
