import os

import discord
from bot import Bot
import ai21


bot = Bot()



class Client(discord.Client):

  async def on_ready(self):
    print("Logged in as", self.user)

  async def answer(self, message):
    history = [f"User: {message.clean_content}"]

    async for historic_msg in message.channel.history(limit=3, before=message):
      if not historic_msg.content:
        continue

      if message.author.name == historic_msg.author.name:
        if isinstance(message.channel, discord.channel.DMChannel):
          name = "User"
        else: # text channel
          for reaction in historic_msg.reactions:
            if str(reaction.emoji) == "❓":
              name = "User"
              break
          else:
            continue

      elif historic_msg.author.name == self.user.name:
        name = "AI21 Discord Bot"
      else:
        continue
      history.insert(0, f"{name}: {historic_msg.clean_content}")

    async with message.channel.typing():
      response = bot.generate(history)
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
