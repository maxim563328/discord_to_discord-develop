import logging
from pyexpat.errors import messages
from telegram.ext import Updater
from telethon import TelegramClient, types

channels_ids = []

updater = Updater(token='5278138253:AAGEkeP2Myhqf_HjcAVyXvrH-ca82j-Epsc', use_context=True)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


api_id = 11541487
api_hash = '05afd9893e288c0d01d4d7fd175cd3a5'
client = TelegramClient('anon', api_id, api_hash)


async def bot_main():
    message = await client.get_messages('https://t.me/python_academy', ids=types.InputMessagePinned())
    return message


if __name__ == '__main__':
    updater.start_polling()