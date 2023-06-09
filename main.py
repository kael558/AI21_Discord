import os

import logging
import traceback

import discord
from bot import Bot
import ai21
import re


async def send_message(channel, reference_msg, message):
    MAX_LENGTH = 2000
    n = len(message)
    first_msg = None
    for i in range(0, n, MAX_LENGTH):
        segment = message[i:i + MAX_LENGTH]
        response_msg = await channel.send(segment, reference=reference_msg,
                                          suppress_embeds=True)
        if not first_msg:
            first_msg = response_msg
    return first_msg


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

    # Remove links
    index = message_cc.find(':link:')
    if index != -1:
        message_cc = message_cc[:index]

    return re.sub('\s+', ' ', message_cc), verbose, no_history


class Client(discord.Client):
    async def on_ready(self):
        with open("avatar.png", "rb") as avatar_file:
            avatar_image = avatar_file.read()
            await client.user.edit(avatar=avatar_image)

        logging.info("Discord bot ready!")
        bot.name = client.get_guild(874538902696914944).get_member(
            client.user.id).display_name

    async def on_member_update(self, before, after):
        if before.id == client.user.id:  # Check if the member is the bot itself
            if before.nick != after.nick:  # Check if the nickname has changed
                if after.nick:  # Check if the bot has a new nickname
                    name = after.nick
                    bot.name = name
                else:
                    bot.name = "QABot"

    async def answer(self, message):
        try:
            users = [message.author.name, bot.name]
            message_cc, verbose, no_history = clean_and_return_options_message(
                message.clean_content)
            history = [f"{message.author.name}: {message_cc}"]
            is_dm_channel = isinstance(message.channel,
                                       discord.channel.DMChannel)

            if not no_history:
                async for historic_msg in message.channel.history(limit=3,
                                                                  before=message):
                    if not historic_msg.content:
                        continue

                    if historic_msg.author.name == self.user.name:
                        if historic_msg.clean_content.startswith(
                                ":information_source:"):
                            continue

                        name = bot.name
                    else:  # message from user
                        if not is_dm_channel:  # if is a text channel
                            for reaction in historic_msg.reactions:
                                if str(reaction.emoji) == "❓":
                                    break
                            else:  # if no question mark reaction, skip
                                continue

                        if historic_msg.author.name not in users:
                            users.append(historic_msg.author.name)
                        name = historic_msg.author.name

                    historic_msg_cc, _, _ = clean_and_return_options_message(
                        historic_msg.clean_content)
                    history.insert(0, f"{name}: {historic_msg_cc}")
            async with message.channel.typing():
                response, verbose_str = bot.generate_response(history, verbose,
                                                              users)

                response_msg = await send_message(message.channel, message,
                                                  response)

                # add thumbs up/thumbs down reaction
                await response_msg.add_reaction("👍")
                await response_msg.add_reaction("👎")

                if verbose:
                    await send_message(message.channel, response_msg,
                                       verbose_str)

                return
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            await message.channel.send(
                "Sorry, an expected error occurred. Please try again later.")

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
        if str(reaction.emoji) == "❓":
            await self.answer(reaction.message)


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(filename='logs/bot.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    bot = Bot(logger=logging)

    logging.info("Attemping to restart Discord Bot...")

    from dotenv import load_dotenv

    load_dotenv()

    ai21.api_key = os.environ['AI21_API_KEY']
    intents = discord.Intents.all()

    client = Client(intents=intents)
    token = os.environ['DISCORD_TOKEN']
    client.run(token)
