import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello! I'm a bot created with aiogram.")

@dp.message(Command("add"))
async def command_add_handler(message: Message) -> None:
    try:
        message_content = message.text.split()
        if (len(message_content) != 3):
            raise Exception()
        _, source, interval = message_content
        await message.answer(f"Source added: {source}")
    except:
        await message.answer("Wrong amount of parameters!")

@dp.message(Command("list"))
async def command_list_handler(message: Message) -> None:
    sources_list = [{"source": "source1", "status": "200 OK"}, {"source": "source2", "status": "502 Bad Gateway"}]
    reply_text = ""

    for element in sources_list:
        reply_text += f"{element['source']} : {element['status']}\n"

    await message.answer(reply_text)    

@dp.message(Command("remove"))
async def command_remove_handler(message: Message) -> None:
    try:
        message_content = message.text.split()
        if (len(message_content) != 2):
            raise Exception()
        _, source_id = message_content
        await message.answer(f"Source {source_id} deleted!")
    except:
        await message.answer("Wrong amount of parameters!")

@dp.message(Command("status"))
async def command_status_handler(message: Message) -> None:
    try:
        message_content = message.text.split()
        if (len(message_content) != 2):
            raise Exception()
        _, source_id = message_content
        await message.answer(f"Source {source_id} status: 200 OK")
    except:
        await message.answer("Wrong amount of parameters!")

@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer("/add https://example.com 60s — добавить ресурс с интервалом проверки,\n"
                        "/list — показать ресурсы и статус,\n"
                        "/remove <id> — удалить,\n"
                        "/status <id> — ручная проверка,\n"
                        "/help — помощь")


# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
          