import ai21


class Bot:

  def __init__(self):
    self.initial_prompt = """
Welcome! I am AI21 Discord Bot, a large language model trained by AI21 Labs, based on the Jurassic architecture. I'm here to help answer your questions, provide advice, or just have a friendly conversation. Please note that while I can provide general information and guidance, I am not a licensed professional and my responses are not intended to be a substitute for professional advice. Additionally, I strive to remain neutral and respectful in all interactions, and I do not engage in discriminatory or harmful behavior. How can I assist you today?
    """
    self.prompt = """
I am AI21 Discord Bot. I'm here to help answer your questions, provide advice, or just have a friendly conversation. Additionally, I strive to remain neutral and respectful in all interactions, and I do not engage in discriminatory or harmful behavior.  

Using the conversation as context, I will write a response to the most RECENT question or statement. 
    """

  def generate(self, history: list):
    if len(history) == 1:
      history.insert(0, self.initial_prompt)
    else:
      history.insert(0, self.prompt)
    history.append("AI21 Discord Bot:")
    history = "\n".join(history)
    print("-----")
    print(history)

    response = ai21.Completion.execute(model="j2-grande-instruct",
                                       prompt=history,
                                       numResults=1,
                                       maxTokens=100,
                                       temperature=0.3,
                                       topKReturn=0,
                                       topP=0.1,
                                       countPenalty={
                                         "scale": 0,
                                         "applyToNumbers": False,
                                         "applyToPunctuations": False,
                                         "applyToStopwords": False,
                                         "applyToWhitespaces": False,
                                         "applyToEmojis": False
                                       },
                                       frequencyPenalty={
                                         "scale": 0,
                                         "applyToNumbers": False,
                                         "applyToPunctuations": False,
                                         "applyToStopwords": False,
                                         "applyToWhitespaces": False,
                                         "applyToEmojis": False
                                       },
                                       presencePenalty={
                                         "scale": 0,
                                         "applyToNumbers": False,
                                         "applyToPunctuations": False,
                                         "applyToStopwords": False,
                                         "applyToWhitespaces": False,
                                         "applyToEmojis": False
                                       },
                                       stopSequences=[])

    return response["completions"][0]['data']['text'].strip()