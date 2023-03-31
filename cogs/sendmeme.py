import aiohttp
import jmespath
import dotenv
import json
import os
from discord import Embed, Colour
from discord.ext import commands


# загружаем значения из dotenv
config = dotenv.dotenv_values(".env")


class Meme(commands.Cog, name="sendmeme"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="memelist", description="get list of memes")
    async def memelist(self, ctx):
        """Отправляем список мемов"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url="https://api.imgflip.com/get_memes") as response: # get запрос
                if response.status == 200:
                    print(f"Status: {response.status}; Everything is fine.")  # если всё норм, то оповещаем

                    data = await response.json()  # сохраняем response как json

                    # записываем мемы и их id в json файл
                    with open("memes_names_and_ids.json", "w", encoding="utf-8") as f:
                        memes_names_and_ids = {}
                        for i in data["data"]["memes"]:
                            memes_names_and_ids[i["name"]] = i["id"]
                        json.dump(memes_names_and_ids, f, ensure_ascii=False, indent=4)


                    list_of_all_memes = jmespath.search("data.memes[*].name", data)  # сохраняем список с названиями мемов
                    # пилю список на две части, т.к нельзя отправить больше 2000 символов
                    list_of_memes1 = list_of_all_memes[:len(list_of_all_memes)//2]
                    list_of_memes2 = list_of_all_memes[len(list_of_all_memes) // 2:]

                    # отправляю два списка по отдельности
                    await ctx.send(f"Список мемесов:\n{', '.join(list_of_memes1)}")
                    await ctx.send(', '.join(list_of_memes2))
                else:
                    # если всё плохо(ответ от сервиса не пришёл, например)
                    print(f"Status: {response.status}; Всйо плохаа")

    @commands.command(name="makememe", description="make your own meme")
    async def makememe(self, ctx, meme_name, top_text=None, bottom_text=None, font="impact", max_font_size="50px"):
        """Делаем мемы, по заданным параметрам"""
        async with aiohttp.ClientSession() as session:
            with open("memes_names_and_ids.json", "r", encoding="utf-8") as f:
                memes_names_and_ids = json.load(f)
            # post запрос
            async with session.post(url="https://api.imgflip.com/caption_image", data={
                "template_id": memes_names_and_ids[meme_name],
                "username": config["imgflip_username"],
                "password": config["imgflip_password"],
                "text0": top_text,
                "text1": bottom_text,
                "font": font,
                "max_font_size": max_font_size
            }) as response:
                if response.status == 200:
                    print(f"Status: {response.status}; Everything is fine.")  # если всё норм, то оповещаем

                    data = await response.json()  # сохраняем response как json

                    # делаю Embed для красоты
                    embed = Embed(title="Your meme!", url=data["data"]["url"], colour=Colour.og_blurple())
                    embed.set_image(url=data["data"]["url"])

                    # Отправляем мем
                    await ctx.send(embed=embed)


# добавляю в коги
async def setup(bot):
    await bot.add_cog(Meme(bot))
