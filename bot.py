import ai21

def dedent(text: str):
    return '\n'.join([m.lstrip() for m in text.split('\n')])
  
class Bot:
  def __init__(self):
    #TODO initialize AI21 labs index info
    pass

  def generate_response(self, conversation_history: list)->str:
    
    conversation_history_str = "\n".join(conversation_history)
    print("History: ")
    print(conversation_history_str)
    preset = choose_preset(conversation_history_str)
    print("PRESET: ", preset)
    
    response_prompt = generate_response_prompt(conversation_history_str, len(conversation_history)==1)
    response = generate_text(response_prompt, preset)
    return response

def generate_response_prompt(conversation: str, first_response: bool):
  if first_response:
    prompt = f"""
      Welcome! I am AI21 Discord Bot, a large language model trained by AI21 Labs, based on the Jurassic architecture. I'm here to help answer your questions, provide advice, or just have a friendly conversation. Please note that while I can provide general information and guidance, I am not a licensed professional and my responses are not intended to be a substitute for professional advice. Additionally, I strive to remain neutral and respectful in all interactions, and I do not engage in discriminatory or harmful behavior. How can I assist you today?  
  
      {conversation}
      AI21 Discord Bot:"""
  else:
    prompt = f"""
    I am AI21 Discord Bot. I'm here to help answer your questions, provide advice, or just have a friendly conversation. Additionally, I strive to remain neutral and respectful in all interactions, and I do not engage in discriminatory or harmful behavior.  

    Using the conversation as context, I will write a response to the most RECENT question or statement.
  
    {conversation}
    AI21 Discord Bot:"""
  return dedent(prompt)



def choose_preset(conversation_history_str: str):
  prompt = choose_preset_prompt(conversation_history_str)
  preset = generate_text(prompt, "Classify NLP task")
  return preset
    
def choose_preset_prompt(conversation: str):
  prompt = f"""
    Using the conversation as context between a bot and a human, classify the most RECENT question or statement to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
    
    User: Who is Canada's favorite figure skating pair?
    AI21 Discord Bot: The most popular pairs figure skaters in Canada are Tessa Virtue and Scott Moir, and Meagan Duhamel and Eric Radford.
    User: When did they win the Olympics?
    
    NLP Task: Question answering   
    ##
    Using the conversation as context between a bot and a human, classify the most RECENT question or statement to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
    
    User: Write me a love poem
    
    NLP Task: Long form generation
    ##
    Using the conversation as context between a bot and a human, classify the most RECENT question or statement to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
    
    User: Describe what Africa is like to visit
    AI21 Discord Bot: Africa is a large and diverse continent, with a wide range of cultures and landscapes. Some popular destinations in Africa include Egypt, South Africa, and Kenya. These countries are known for their ancient civilizations, vibrant cities, and stunning natural beauty. Africa is also home to a number of national parks and reserves, including the Sahara Desert, the Serengeti, and the Ngorongoro Crater. These areas offer visitors the opportunity to experience Africa's rich wildlife and unique ecosystems. Overall, Africa is a fascinating place to visit, and it offers visitors a unique and unforgettable experience.
    User: Can you write a shorter description of that and focus on the culture?
    
    NLP Task: Paraphrasing
    ##
    Using the conversation as context between a bot and a human, classify the most RECENT question or statement to one of the following NLP tasks: Generate code, Paraphrasing, Long form generation, Question answering
    
    {conversation}
    
    NLP Task:
    """
  return dedent(prompt)
  







def get_params_from_preset(preset: str) -> dict:
  # TODO Check presence penalties
  if preset == "Classify NLP task":
    return {
      "model_name": "j2-large",
      "maxTokens": 55,
      "temperature": 0,
      "topP": 1,
      "stopSequences": ["##"]
    }

  
  if preset == "Generate code":
    return {
      "model_name": "j2-large",
      "maxTokens": 100,
      "temperature": 0,
      "topP": 1,
    }

  if preset == "Paraphrasing":
    return {
      "model_name": "j2-jumbo",
      "maxTokens": 100,
      "temperature": 0.4,
      "topP": 1,
    }
    
  if preset == "Long Form Generation":
    return {
      "model_name": "j2-jumbo-instruct",
      "maxTokens": 300,
      "temperature": 0.84,
      "topP": 1,
    }
  

  if preset == "In-Context QA":
    return {
      "model_name": "j2-jumbo-instruct",
      "maxTokens": 70,
      "temperature": 0,
      "topP": 1,
    }

  
  if preset == "QA":
    return {
      "model_name": "j2-jumbo-instruct",
      "maxTokens": 70,
      "temperature": 0.8,
      "topP": 1,
    }
  
    
  return {
      "model_name": "j2-grande-instruct",
      "maxTokens": 200,
      "temperature": 0.7,
      "topP": 1,
    }

def get_default_preset_params():
  return {
    "model_name": "j2-grande-instruct",
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
    "frequencyPenalty":{
       "scale": 0,
       "applyToNumbers": False,
       "applyToPunctuations": False,
       "applyToStopwords": False,
       "applyToWhitespaces": False,
       "applyToEmojis": False
    },
    "presencePenalty":{
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
  
  response = ai21.Completion.execute(prompt=prompt, **params)
  return response["completions"][0]['data']['text'].strip()

  

    