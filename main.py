# coding=utf-8
import os
import asyncio
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

import logging

# Configure logging
# logging.basicConfig(level=logging.DEBUG)

# intents.message_content = True
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 移除原本的help指令
bot.remove_command("help")

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# 當機器人完成啟動時
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        for item in synced:
            print(f"load {item}")
    except Exception as e:
        print(e)
    print(f"目前登入身份 --> {bot.user}")

# 一開始bot開機需載入全部程式檔案
async def load_extensions(directory="cogs"):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                extension = os.path.relpath(os.path.join(root, file), directory).replace(os.sep, ".")[:-3]
                await bot.load_extension(f"cogs.{extension}")                 

async def main():
  async with bot:
    await load_extensions()   
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
  asyncio.run(main())