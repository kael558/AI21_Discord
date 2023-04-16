import os

import ai21
import discord


def generate(prompt: str):
  response = ai21.Completion.execute(model="j2-grande-instruct",
                                     prompt=prompt,
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


class Client(discord.Client):

  async def on_ready(self):
    print("Logged in as", self.user)

  async def answer(self, message):
    async with message.channel.typing():
      response = generate(message.clean_content)
      response_msg = await message.channel.send(response, reference=message)
      await response_msg.edit(suppress=True)
      return

  async def on_message(self, message):
    # Ignore messages from itself to avoid infinite loops
    if message.author == self.user:
      return

    # Check if the message is a direct message
    if isinstance(message.channel, discord.channel.DMChannel):
      await self.answer(message)

  async def on_reaction_add(self, reaction, user):
    # Check if the user is the bot itself
    if user == self.user:
      return

    # Check if the reaction is a single question mark
    if str(reaction.emoji) == "❓" and reaction.count == 1:
      await self.answer(reaction.message)


if __name__ == "__main__":
  ai21.api_key = os.environ['AI21_API_KEY']
  intents = discord.Intents.all()

  client = Client(intents=intents)
  token = os.environ['DISCORD_TOKEN']
  client.run(token)
