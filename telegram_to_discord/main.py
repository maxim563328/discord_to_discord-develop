from telethon import TelegramClient, types, sync

# Use your own values from my.telegram.org
api_id = 11541487
api_hash = '05afd9893e288c0d01d4d7fd175cd3a5'

client = TelegramClient('anon', api_id, api_hash)


async def bot_main():
    me = await client.get_me()
    print(me.stringify())
    await client.send_message('+79832313130', 'Hello, friend!')
    message = await client.get_messages('https://t.me/python_academy', ids=types.InputMessagePinned())
    print(message)


def main():
    with client:
        client.loop.run_until_complete(bot_main())
