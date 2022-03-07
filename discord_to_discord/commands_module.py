from attr import has
import requests
from telethon import TelegramClient, functions, types, errors


def check_command_tg_type(command_text):
    if len(command_text) < 2:
        return 0
    if command_text[1][0] == "@":
        return 300
    if command_text[1][0] == "https":
        return 301    
    else:
        return False


def check_valid_add(command_text):
    if len(command_text) < 4:
        return 0    
    if not command_text[1].isdigit():
        return 1
    if not command_text[2].isdigit():
        return 2
    if not command_text[3].isdigit():
        return 3

    data = {
        "server_get": int(command_text[1]),
        "server_take": int(command_text[2]),
        "take_channel": int(command_text[3]),
    }

    r = requests.get("https://discord.com/api/v9/users/@me/guilds?token=Njk2NzE5NDUxMjE4OTAzMTIw.YiImfg._LAPZFQ8vRQQzp_7H3_YEpRzDUE")
    data_new = r.json()

    for element in data_new:
        if data["server_get"] == int(element["id"]):
            break
    else:
        return 10
    for element in data_new:
        if data["server_get"] == int(element["id"]):
            break
    else:
        return 11

    for element in data_new:
        if data["server_get"] == int(element["id"]):
            break
    else:
        return 12

    return data


def check_valid_rem(command_text):
    if len(command_text) < 2:
        return 0    
    if not command_text[1].isdigit():
        return 1
    r = requests.get("https://discord.com/api/v9/users/@me/guilds?token=Njk2NzE5NDUxMjE4OTAzMTIw.YiImfg._LAPZFQ8vRQQzp_7H3_YEpRzDUE")
    data_new = r.json()
    for element in data_new:
        if int(command_text[1]) == int(element["id"]):
            break
    else:
        return 10
    return {"server_get": int(command_text[1])}