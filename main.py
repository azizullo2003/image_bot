from aiogram import Bot, Dispatcher, executor
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage

BOT_TOCKEN = '5379980890:AAGXlFmKl34U-nEWGNGGa1_sXeVsjC-1vKQ'

loop = asyncio.new_event_loop()
bot = Bot(token=BOT_TOCKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)

if __name__ == "__main__":
    from bot import dp
    from AlbumMiddleware import AlbumMiddleware

    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)
