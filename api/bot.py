"""
the main @client.event file for the bot, will use the triggers.py file to trigger the bot and do the
necessary processing for the data
"""
import os
import dotenv
import discord
import logging

from api.commands.triggers import (
    qna_trigger,
    qna_action,
    mention_trigger,
    reply_trigger,
)


# get token from .env
dotenv.load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# create the client
intents = discord.Intents.default()
intents.message_content = True

DISCORD_CLIENT = discord.Client(intents=intents)


@DISCORD_CLIENT.event
async def on_ready():
    logging.info(f'We have logged in as {DISCORD_CLIENT.user}')
    print(f'We have logged in as {DISCORD_CLIENT.user}')


@DISCORD_CLIENT.event
async def on_message(message):
    # ignore messages from the bot itself
    if message.author == DISCORD_CLIENT.user:
        return

    # triggers the LLM QnA response
    elif response := await reply_trigger(message, DISCORD_CLIENT):
        history = response[1]
        pymon_response = qna_action(message, DISCORD_CLIENT, history=history)
        if len(pymon_response) > 2000:
            # split into multiple messages
            for i in range(0, len(pymon_response), 2000):
                await message.reply(pymon_response[i:i + 2000])
        else:
            await message.reply(pymon_response)

    elif qna_trigger(message):
        pymon_response = qna_action(message)
        if len(pymon_response) > 2000:
            # split into multiple messages
            for i in range(0, len(pymon_response), 2000):
                await message.reply(pymon_response[i:i + 2000])
        else: 
            await message.reply(pymon_response)

    # automatically replies with LLM if bot is being replied to or tagged
    elif mention_trigger(DISCORD_CLIENT, message) :
        is_reply = await reply_trigger(message, DISCORD_CLIENT)
        if not is_reply:
            pymon_response = qna_action(message, DISCORD_CLIENT)
            if len(pymon_response) > 2000:
                # split into multiple messages
                for i in range(0, len(pymon_response), 2000):
                    await message.reply(pymon_response[i:i + 2000])
            else:
                await message.reply(pymon_response)
