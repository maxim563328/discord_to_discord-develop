import threading
import discord_to_discord.main as ds_bot
import telegram_to_discord.main as tg_bot

if __name__ == '__main__':
    discord_bot = threading.Thread(target=ds_bot.main())
    telegram_bot = threading.Thread(target=tg_bot.main())
    
    discord_bot.start()
    telegram_bot.start()