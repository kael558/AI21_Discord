import argparse
import ai21
import discord

parser = argparse.ArgumentParser(description="A QA bot for discord with AI21.")
parser.add_argument("--ai21_api_key", type=str, help="api key for AI21", required=True)
parser.add_argument("--discord_key", type=str, help="api key for discord bot", required=True)

args = parser.parse_args()


def generate(prompt: str):
    response = ai21.Completion.execute(
        model="j2-grande-instruct",
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
        stopSequences=[]
    )

    if 'completions' not in response or response['completions'][0]['data']['text'] == '' or \
            response['completions'][0]['data']['text'].isspace():
        return None

    return response['completions'][0]['data']['text'].strip()


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
        if user != self.user:
            return

        # Check if the reaction is a single question mark
        if str(reaction.emoji) == "❓" and reaction.count == 1:
            await self.answer(reaction.message)


if __name__ == "__main__":
    intents = discord.Intents.all()
    client = Client(intents=intents)
    client.run(args.discord_key)
