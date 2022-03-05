from discord import File
import os
import discord
import sqlite3 as sq
import content_fetcher

from disnake import ChannelType
import commands_module
from discord.ext import commands


intents = discord.Intents.all()

client = commands.Bot(
    command_prefix="$", intents=intents)


users_data = {
    "accessed_accounts": {
        420989301170634762: {
        }
        }
}

with sq.connect(r'database.db') as con:
    con = con
    cur = con.cursor()


@client.event
async def on_ready():
    name = client.user.name + '#' + client.user.discriminator

    print(f"""#                             
#     Доброго пожаловать!     
#                             
#     Бот успешно запущен!    
#     Имя бота: {name}        
#                          
""")


@client.event
async def on_message(message):
    if message.content.split(' ')[0] == "$rem-server":
        if message.author.id not in users_data["accessed_accounts"].keys():
            return
        command_text = message.content.split(' ')
        data = commands_module.check_valid_rem(command_text)
        if data == 0:
            await message.channel.send(f"**Вы не написали ID сервера, который надо удалить ❌**")
            return
        if data == 1:
            await message.channel.send(f"**ID сервера должно быть целочисленным, а не - `{command_text[1]}` ❌**")
            return
        if data == 10:
            await message.channel.send(f"**Бот не находится на сервере с ID - `{command_text[1]}`, пожалуйста, проверьте корректность ID ❌**")
            return
        cur.execute("DELETE FROM server_list WHERE server_get=?", (int(command_text[1])))        
        con.commit()
        await message.channel.send("**Удаление успешно выполнено. ✅**")
    if message.content.split(' ')[0] == "$set-server":
        if message.author.id not in users_data["accessed_accounts"].keys():
            return
        command_text = message.content.split(' ')
        data = commands_module.check_valid_set(command_text)
        if data == 0:
            await message.channel.send(f"**Какой то из аргументов упущен, принято аргументов - {len(command_text) - 1}/3 ❌**")
            return
        if data == 1:
            await message.channel.send(f"**ID сервера для _отслеживания_ сообщений должно быть целочисленным, а не - `{command_text[1]}` ❌**")
            return
        if data == 2:
            await message.channel.send(f"**ID сервера для _отправки_ сообщений должно быть целочисленным, а не - `{command_text[2]}` ❌**")
            return
        if data == 3:
            await message.channel.send(f"**ID канала для _отправки_ сообщений должно быть целочисленным, а не - `{command_text[3]}` ❌**")
            return
        if data == 10:
            await message.channel.send(f"**Бот не находится на сервере с ID - `{command_text[1]}`, пожалуйста, проверьте корректность ID ❌**")
            return
        if data == 11:
            await message.channel.send(f"**Бот не находится на сервере с ID - `{command_text[2]}`, пожалуйста, проверьте корректность ID ❌**")
            return
        if data == 12:
            await message.channel.send(f"**Бот не находится на сервере с ID - `{command_text[3]}`, пожалуйста, проверьте корректность ID ❌**")
            return
        cur.execute("INSERT INTO server_list(server_get, server_take, take_channel) VALUES (?, ?, ?)", (data["server_get"], data["server_take"], data["take_channel"]))        
        con.commit()
        await message.channel.send("**Внесенные данные успешно сохранены. ✅**")


    if message.channel.type != ChannelType.text:
        return

    # get server-to-check data
    cur.execute("SELECT server_get FROM server_list")
    servers_ids = cur.fetchall()
    for id in servers_ids:
        if id[0] == message.channel.guild.id:
            guild = id[0]
            break
    else:
        return
    cur.execute("SELECT server_take FROM server_list WHERE server_get = ?", (guild,))
    guild_s = cur.fetchall()[0][0]
    cur.execute("SELECT take_channel FROM server_list WHERE server_get = ? AND server_take = ?", (guild, guild_s))
    channel = cur.fetchall()[0][0]
    channel = client.get_channel(channel)
    data = {
    "server_get": message.guild.id,
    "server_get_channel": message.channel.id,
    "last_id": message.id
    }


    # get message vontent
    content = content_fetcher.main(data)
    print(content)
    if content == '':
        return
    if content == 403:
        await channel.send("**[Новое сообщение]**\nСервер | **{}**\nКанал | `{}`\nАвтор | `{}`\nСодержание не удалось захватить".format(message.author.guild.name, message.channel.name, message.author, content["text"]))
        return
    if "img" in content.keys() and content["img"]["url"] != "":
        if 405 in content["img"]["errors"]:
            await channel.send("**[Новое сообщение]**\nСервер | **{}**\nКанал | `{}`\nАвтор | `{}`\nСодержание: {}".format(message.author.guild.name, message.channel.name, message.author, content["text"] + " " + content["img"]["url"]))
        else:
            for root, dirs, files in os.walk("/attachments"):
                for file in files:  
                    if content["img"]["file_id"] in file:
                        global path
                        path = f"/attachments/{file}"
                        break
                else:
                    await channel.send("**[Новое сообщение]**\nСервер | **{}**\nКанал | `{}`\nАвтор | `{}`\nСодержание: {}".format(message.author.guild.name, message.channel.name, message.author, content["text"] + " " + content["img"]["url"]))
                    return
            await channel.send("**[Новое сообщение]**\nСервер | **{}**\nКанал | `{}`\nАвтор | `{}`\nСодержание: {}".format(message.author.guild.name, message.channel.name, message.author, content["text"]), file=File(path))
    else:
        await channel.send("**[Новое сообщение]**\nСервер | **{}**\nКанал | `{}`\nАвтор | `{}`\nСодержание: {}".format(message.author.guild.name, message.channel.name, message.author, content["text"]))


client.run("Njk2NzE5NDUxMjE4OTAzMTIw.YiImfg._LAPZFQ8vRQQzp_7H3_YEpRzDUE", bot=False)