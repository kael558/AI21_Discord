import os

import logging

import discord
from bot import Bot
import ai21

bot = Bot()

# Set up logging
logging.basicConfig(filename='logs/bot.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def clean_and_return_options_message(message_cc: str) -> tuple:
    verbose, no_history = False, False

    while True:
        message_cc = message_cc.strip()
        if message_cc.endswith('--verbose'):
            verbose = True
            message_cc = message_cc.replace('--verbose', '')
            continue
        if message_cc.endswith('--no-history'):
            no_history = True
            message_cc = message_cc.replace('--no-history', '')
            continue
        if message_cc.endswith('-v'):
            verbose = True
            message_cc = message_cc.replace('-v', '')
            continue
        if message_cc.endswith('-nh'):
            no_history = True
            message_cc = message_cc.replace('-nh', '')
            continue
        break
    message_cc = message_cc.strip()
    return message_cc, verbose, no_history


class Client(discord.Client):
    async def on_ready(self):
        logging.info("Discord bot ready!")
        print("Peon: Ready to work!", self.user)

    async def answer(self, message):
        try:
            message_cc, verbose, no_history = clean_and_return_options_message(message.clean_content)

            history = [f"User: {message_cc}"]
            if not no_history:
                async for historic_msg in message.channel.history(limit=5, before=message):
                    if not historic_msg.content:
                        continue

                    if message.author.name == historic_msg.author.name:
                        if isinstance(message.channel, discord.channel.DMChannel):
                            name = "User"
                        else:  # is text channel
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
                    historic_msg_cc, _, _ = clean_and_return_options_message(historic_msg.clean_content)
                    history.insert(0, f"{name}: {historic_msg_cc}")

            async with message.channel.typing():
                response = bot.generate_response(history, verbose)
                response_msg = await message.channel.send(response, reference=message)
                await response_msg.edit(suppress=True)
                return
        except Exception as e:
            logging.error(e)
            await message.channel.send("Sorry, an expected error occurred. Please try again later.")

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
    logging.info("Attemping to restart Discord Bot...")
    from dotenv import load_dotenv
    load_dotenv()

    ai21.api_key = os.environ['AI21_API_KEY']
    intents = discord.Intents.all()

    client = Client(intents=intents)
    token = os.environ['DISCORD_TOKEN']
    client.run(token)
