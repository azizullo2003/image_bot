from main import bot, dp
from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from typing import List
from generation_qr_code import gen_qr_code
from pathlib import Path


class Text(StatesGroup):
    text = State()


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Привет! Пришли мне сначала картинку, а потом текст и я сделаю из этого QR-Code!",
                           reply_to_message_id=message.message_id)


@dp.message_handler(content_types=['text'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Привет! Пришли мне сначала картинку, а потом текст и я сделаю из этого QR-Code!",
                           reply_to_message_id=message.message_id)


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message, album: List[types.Message] = None):
    global path_to_download
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("Без текста"))
    if message.media_group_id is None:
        await message.photo[-1].download(
            destination_file=f'C:/Users/TaNik/photos/{(str(message.date).replace(":", ".")).replace("-", ".")}/1.jpg')
        src = f'C:/Users/TaNik/photos/{(str(message.date).replace(":", ".")).replace("-", ".")}/'
        path_to_download = Path().joinpath(src)  # Путь до фона qr кода
        print(path_to_download)
        await bot.send_message(message.from_user.id, "Фото получено! Отправьте текст!",
                               reply_to_message_id=message.message_id, reply_markup=markup)
    else:
        for cnt, obj in enumerate(album):
            if obj.photo:
                await obj.photo[-1].download(
                    destination_file=f'C:/Users/TaNik/photos/{(str(message.date).replace(":", ".")).replace("-", ".")}/{cnt + 1}.jpg')
        src = f'C:/Users/TaNik/photos/{(str(message.date).replace(":", ".")).replace("-", ".")}/'
        path_to_download = Path().joinpath(src)
        await bot.send_message(message.from_user.id, "Фотографии получены! Отправьте текст!",
                               reply_to_message_id=message.message_id, reply_markup=markup)
    await Text.text.set()


@dp.message_handler(state=Text.text)
async def handle_docs_photo(message: types.Message, state: FSMContext):
    global path_to_download
    path_to_save = Path().joinpath("qr_code.png")
    gen_qr_code(str(path_to_download), path_to_download, path_to_save)
    if message.text != "Без текста":
        await bot.send_message(message.from_user.id, 'Ваш текст принят!\nОжидайте.',
                               reply_to_message_id=message.message_id)
        my_file = open(f"{path_to_download}/текст.txt", "w+")
        my_file.write(message.text)
        my_file.close()
    with open('qr_code.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)

        await bot.send_message(message.chat.id, 'Ваш QR-Code готов!')
    await state.finish()
