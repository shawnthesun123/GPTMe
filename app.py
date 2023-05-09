import os

import discord
import openai
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')


defaultMessage = [{"role": "system", "content": "You are a helpful, but straight to the point AI Coding assistant."}]
messages = defaultMessage
defaultUser = ""
curr_user = defaultUser


@bot.command(name='gpt')
async def gpt_command(ctx, *, userText):
    global curr_user, messages
    if userText == "reset":
        messages = defaultMessage
        await ctx.send("Bot has been reset")
    elif userText == "reset user":
        curr_user = defaultUser
        await ctx.send("User has been reset")
    elif userText == "reset all":
        messages = defaultMessage
        curr_user = defaultUser
        await ctx.send("Reset All")

    if curr_user == "":
        curr_user = ctx.author.name

    print(f'User: {curr_user}')

    if ctx.author.name == curr_user:
        messages.append({"role": "user", "content": userText})

        # Use the OpenAI API to generate a response to the message
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        # Send the response as a message
        await ctx.send(reply)
    else:
        await ctx.send("You weren't the first user")


# Start the bot
bot.run(TOKEN)
