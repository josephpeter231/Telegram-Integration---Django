import asyncio
from telegram import Bot
from telegram.ext import Application

TOKEN = "your token "
chat_id = 1814948590  # Replace with your actual chat ID

async def send_message(text, chat_id):
    # Initialize the bot with the token
    bot = Bot(token=TOKEN)
    
    # Send the message asynchronously
    await bot.send_message(chat_id=chat_id, text=text)

async def main():
    # Sending a message
    await send_message(text='Hi Sujit!, How are you?', chat_id=chat_id)

if __name__ == '__main__':
    asyncio.run(main())
