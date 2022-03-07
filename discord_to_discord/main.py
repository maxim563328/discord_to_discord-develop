from ctypes import util
from tabnanny import check
import discord
import sqlite3 as sq
import requests
import asyncio
import commands_module as commands_module
import random
import string
import os

from disnake import ChannelType
from discord import File
from discord.ext import commands, tasks
from telethon.tl.types import InputMessagePinned
from telethon.tl.functions.channels import GetChannelsRequest
from telethon.tl.types import InputChannel
from telethon.tl.types.messages import ChatFull

from telethon import TelegramClient, types, errors, functions, utils

intents = discord.Intents.all()
client = commands.Bot(
    command_prefix="$", intents=intents)

api_id = 11541487
api_hash = '05afd9893e288c0d01d4d7fd175cd3a5'
client_tg = TelegramClient('anon', api_id, api_hash)


users_data = {
    "accessed_accounts": {
        420989301170634762: {
        }
    }
}


with sq.connect(r'database.db') as con:
    con = con
    cur = con.cursor()


@tasks.loop(minutes=2.0)
async def check_telegram_pin_msg():
    cur.execute("SELECT * FROM tg_channels")
    res = cur.fetchall()
    if res == []:
        return
    channel = client.get_channel(696285756225749026)
    for chat in res:
        channel_tg, content = await get_pinned_tg_message(chat[0], chat[1])
        await channel.send(f"**[Новое закрепленное сообщение]\nКанал: `{channel_tg.title}`**\nСодержание:\n.\n.\n.\n{content.message}")


@client.event
async def on_ready():
    name = client.user.name + '#' + client.user.discriminator
    check_telegram_pin_msg.start()
    print(f"""#
#     Доброго пожаловать!
#
#     Бот успешно запущен!
#     Имя бота: {name}
#
""")


@client.event
async def on_message(message):
    if message.content.split(' ')[0] == "$add-tg-channel":
        if message.author.id not in users_data["accessed_accounts"].keys():
            return
        command_text = message.content.split(' ')
        checker = commands_module.check_command_tg_type(command_text)
        if checker == 0:
            await message.channel.send("**Вы не указали канал телеграм ❌**")
            return
        elif checker == 301:
            data = await check_valid_tg_add_link(command_text)
        elif checker == 300:
            data = await check_valid_tg_add_decorator(command_text)
            if data == 404:
                await message.channel.send("**Канал не найден, проерьте правильность введенного @логина ❌**")
                return
            if type(data) != types.Channel:
                await message.channel.send("**Чат, приглашение на которой вы прислали, не является каналом ❌**")
                return
        else:
            await message.channel.send("**Вы не верно указали канал телеграм ❌**")
            return
        if data == 0:
            await message.channel.send("**Вы не указали канал телеграм ❌**")
            return
        if data == 11:
            await message.channel.send("**Указанное вами приглашение больше не действительно ❌**")
            return
        if data == 12:
            await message.channel.send("**Чат, приглашение которого вы присылали, не существует ❌**")
            return
        if type(data) != types.Channel:
            if data.channel is False:
                await message.channel.send("**Чат, приглашение на которой вы прислали, не является каналом ❌**")
                return
            if data.public is False:
                await message.channel.send("**Канал, который вы прислали, является закрытым ❌**")
                return
            if commands_module.check_in_data_base(data.chat.id, "tg_channels", "channel_id") == 1:
                await message.channel.send("**Данный канал уже есть в базе данных ❌**")
                return
            cur.execute("INSERT INTO tg_channels VALUES(?, ?)",
                        (data.id, data.access_hash))
            con.commit()
        else:
            if commands_module.check_in_data_base(data.id, "tg_channels", "channel_id") == 1:
                await message.channel.send("**Данный канал уже есть в базе данных ❌**")
                return
            cur.execute("INSERT INTO tg_channels VALUES(?, ?)",
                        (data.id, data.access_hash))
            con.commit()
        await message.channel.send(f"**Канал `{data.title}` успешно сохранён ✅**")

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
        if commands_module.check_in_data_base(int(command_text[1]), "server_list", "server_get") == 0:
            await message.channel.send("**Данного сервера нет в базе данных ❌**")
            return
        cur.execute("DELETE FROM server_list WHERE server_get=?",
                    (int(command_text[1])))
        con.commit()
        await message.channel.send("**Удаление успешно выполнено ✅**")
    if message.content.split(' ')[0] == "$add-server":
        if message.author.id not in users_data["accessed_accounts"].keys():
            return
        command_text = message.content.split(' ')
        data = commands_module.check_valid_add(command_text)
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
        if commands_module.check_in_data_base(data["server_get"], "server_list", "server_get") == 1:
            await message.channel.send("**Данный сервер уже есть в базе данных ❌**")
            return
        cur.execute("INSERT INTO server_list(server_get, server_take, take_channel) VALUES (?, ?, ?)",
                    (data["server_get"], data["server_take"], data["take_channel"]))
        con.commit()
        await message.channel.send("**Внесенные данные успешно сохранены ✅**")

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
    cur.execute(
        "SELECT server_take FROM server_list WHERE server_get = ?", (guild,))
    guild_s = cur.fetchall()[0][0]
    cur.execute(
        "SELECT take_channel FROM server_list WHERE server_get = ? AND server_take = ?", (guild, guild_s))
    channel = cur.fetchall()[0][0]
    channel = client.get_channel(channel)
    data = {
        "server_get": message.guild.id,
        "server_get_channel": message.channel.id,
        "last_id": message.id
    }
    await asyncio.sleep(1)
    r = requests.get(
        f"https://discord.com/api/v9/channels/{message.channel.id}/messages?token=Njk2NzE5NDUxMjE4OTAzMTIw.YiImfg._LAPZFQ8vRQQzp_7H3_YEpRzDUE")
    data = r.json()
    for msg in data:
        if int(msg["id"]) == message.id:
            message_ = msg

    if message_["attachments"] != []:
        path = 'attachments/' + download_attachment(message_["attachments"][0]["proxy_url"], message_[
                                                    "attachments"][0]["filename"], message_["attachments"][0]["content_type"], message_["attachments"][0]["size"])
        await channel.send("**[Новое сообщение]**\nСервер | **{}**\nКанал | `{}`\nАвтор | `{}`\nСодержание: {}".format(message.author.guild.name, message.channel.name, message.author, message_["content"]), file=File(path))
        os.remove(path)
        return
    await asyncio.sleep(1)
    await channel.send("**[Новое сообщение]**\nСервер | **{}**\nКанал | `{}`\nАвтор | `{}`\nСодержание: {}".format(message.author.guild.name, message.channel.name, message.author, message_["content"]))


def download_attachment(url: str, filename: str, content_type: str, size: int):
    file_id = "_" + "".join(random.choices(string.ascii_uppercase +
                            string.digits + string.ascii_lowercase, k=6))
    filename = filename.split('.')[0] + file_id + '.' + filename.split('.')[1]
    r = requests.get(url, allow_redirects=True)
    open(f'attachments/{filename}', 'wb').write(r.content)
    return filename


async def check_valid_tg_add_link(command_text):
    async with client_tg:
        if len(command_text) < 2:
            return 0
        hash_tg = command_text[1].split('/')[-1]
        try:
            result = await client_tg(functions.messages.CheckChatInviteRequest(hash=hash_tg))
        except errors.InviteHashExpiredError:
            return 11
        except errors.InviteHashInvalidError:
            return 12
        return result


async def check_valid_tg_add_decorator(command_text):
    async with client_tg:
        if len(command_text) < 2:
            return 0
        try:
            peer = await client_tg.get_entity(command_text[1])
        except:
            return 404
        return peer


async def get_pinned_tg_message(id_: int, hash_: int):
    async with client_tg:
        channel = InputChannel(id_, hash_)
        message = await client_tg.get_messages(channel, ids=InputMessagePinned())
        new_channel = await client_tg(
            functions.channels.GetChannelsRequest(id=[id_]))
        print(new_channel.chats[0])
        return new_channel.chats[0], message


if __name__ == '__main__':
    client.run(
        "Njk2NzE5NDUxMjE4OTAzMTIw.YiImfg._LAPZFQ8vRQQzp_7H3_YEpRzDUE", bot=False)
