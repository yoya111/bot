import logging
import random
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


TOKEN = "6250291566:AAFlfElzrBTh4hrFQrkrJyfNmupqexx0g-c"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

@dp.message_handler(lambda message: message.text == 'Танцуй как он')
async def porn_site(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="https://matias.ma/nsfw/")


@dp.message_handler(lambda message: message.text == 'Анекдот')
async def anekdot_handler(message: types.Message):
    response = requests.get('https://www.anekdot.ru/random/anekdot/')
    soup = BeautifulSoup(response.content, 'html.parser')
    anekdot = soup.find_all('div', {'class': 'text'})[0].text.strip()
    await bot.send_message(message.chat.id, anekdot)

@dp.message_handler(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await message.reply("Введите пароль:")
    await state.set_state("password")


@dp.message_handler(state="password")
async def password_handler(message: types.Message, state: FSMContext):
    if message.text == "123":
        await message.reply("Пароль верный.")
        await state.finish()
        user_full_name = message.from_user.full_name
        await message.reply(f"Привет, {user_full_name}! Чтобы открыть меню, воспользуйтесь командой /menu.")
    else:
        await message.reply("Пароль неверный.")


@dp.message_handler(commands=["menu"])
async def menu_handler(message: types.Message):
    await message.reply("Выберите действие:", reply_markup=get_menu_keyboard())


@dp.message_handler(lambda message: message.text == 'Случайное число')
async def process_message_random(message: types.Message):
    random_number = random.randint(0, 100)
    await bot.send_message(message.chat.id, f"Случайное число: {random_number}")


@dp.message_handler(lambda message: message.text == 'НАСТЯ')
async def nastya_handler(message: types.Message):
    await bot.send_message(message.chat.id, "ТЫ САМАЯ ЛУЧШАЯ!")


@dp.message_handler(lambda message: message.text == 'Выход')
async def exit_handler(message: types.Message):
    await message.reply("Вы вышли из меню.", reply_markup=get_main_keyboard())


@dp.message_handler(lambda message: message.text == 'Limonch')
async def limonch_handler(message: types.Message):
    await bot.send_message(message.chat.id,  "Понедельник - отхода\nВторник - отхода\nСреда - отхода\nЧетверг - отхода\nСуббота - Закупка\nВоскресенье - УРААААА ЛИМОНЧЕЛИМСЯ!!!")


def get_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    random_button = KeyboardButton("Случайное число")
    nastya_button = KeyboardButton("НАСТЯ")
    limonch_button = KeyboardButton("Limonch")
    exit_button = KeyboardButton("Выход")
    anekdot_button = KeyboardButton("Анекдот")
    dance_button = KeyboardButton("Танцуй как он")
    keyboard.add(random_button, nastya_button)
    keyboard.add(limonch_button, anekdot_button)
    keyboard.add(dance_button)
    keyboard.add(exit_button)
    return keyboard


def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = KeyboardButton("/menu")
    keyboard.add(menu_button)
    return keyboard


if __name__ == "__main__":
    executor.start_polling(dp)



