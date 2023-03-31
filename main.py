import asyncio
import os
import logging
import discord
from discord.ext import commands
import dotenv

# загружаем значения из dotenv
config = dotenv.dotenv_values(".env")

# назначаем боту права(пока что все, поменяю позже)
intents = discord.Intents.all()
intents.message_content = True

# выдаю боту префикс $, выдаю права
bot = commands.Bot(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents)

# логи(пока просто скопировал код с темплейта, потом разберусь как с ними работать)
logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
bot.logger = logger


@bot.event
async def on_ready():
    """Когда бот запустился, то делаем вот это вот"""
    bot.logger.info(f"Logged in as {bot.user.name}")  # оповещаем о запуске бота


async def load_cogs():
    """Загружаем коги"""
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):  # проходимся по папке cogs
        if file.endswith(".py"):  # берём все .py файлики
            extension = file[:-3]  # сохраняем расширение
            try:
                await bot.load_extension(f"cogs.{extension}")  # загружаем коги
            except Exception as e:  # обработочка исключений
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


# запускаем
asyncio.run(load_cogs())
bot.run(config["TOKEN"])
