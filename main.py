from aiogram import Bot, Dispatcher, types, executor
from db import Database
from io import BytesIO
from datetime import date
import logging
import config
import keyboard as kb
import qrcode

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

db = Database('park_db.db')


def make_qrcode(text):
    buf = BytesIO()
    qrcode.make(text).save(buf, format='PNG')
    buf.seek(0)
    return types.InputFile(buf, "qrcode.png")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        db.set_nickname(message.from_user.id, message.from_user.full_name)
        db.set_time_sub(message.from_user.id, date.today())
        await message.answer(f"Добро пожаловать в систему FPS, если нужна помощь отправь /help", reply_markup=kb.menu)
    else:
        await message.answer(f"Привет {db.get_nickname(message.from_user.id)}!", reply_markup=kb.menu)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer("Данный бот является частью системы Fanov Parking Services\n"
                         "Для аренды места - Парковки🚗>>>Город>>>Место\n"
                         "Наш сайт - https://jienivets.github.io/FanovParkingServices/pages/parcing.html\n"
                         "По всем вопросам - @ijstt_resurrected")


@dp.message_handler(text=['Профиль👤'])
async def profile(message: types.Message):
    await message.answer("Ваш профиль:", reply_markup=kb.profile)
    await message.answer(f"Ваш ник - {db.get_nickname(message.from_user.id)}\n"
                         f"Ваш балансе - {db.get_balance(message.from_user.id)} рублей\n"
                         f"Дата регистрации - {db.get_time_sub(message.from_user.id)}", reply_markup=kb.balance)


@dp.message_handler(text=['Обратиться в тех поддержку📱'])
async def send_help(message: types.Message):
    await message.answer("@ijstt_resurrected")


@dp.message_handler(text=['Назад⬅️'])
async def back(message: types.Message):
    await message.answer("Вы вернулись в главное меню", reply_markup=kb.menu)


@dp.message_handler(text=['Парковки🚗'])
async def back(message: types.Message):
    await message.answer("Выберите город", reply_markup=kb.cities)


@dp.callback_query_handler(lambda x: x.data == 'lipetsk')
async def lipetsk(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text="Выберите парковку:", reply_markup=kb.lip_parks)


@dp.callback_query_handler(lambda x: x.data == 'lp1')
async def lp1(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text="#1 — Коммунальная площадь, Липецк")
    await bot.send_location(callback_query.from_user.id, 52.601416, 39.589620)
    await bot.send_message(callback_query.from_user.id, text="Всего мест - 30\nСвободных мест - ...",
                           reply_markup=kb.lp_book)


@dp.callback_query_handler(lambda x: x.data == 'lp2')
async def lp1(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text="#2 — площадь Петра Великого, Липецк")
    await bot.send_location(callback_query.from_user.id, 52.603981, 39.600361)
    await bot.send_message(callback_query.from_user.id, text="Всего мест - 30\nСвободных мест - ...",
                           reply_markup=kb.lp_book)


@dp.callback_query_handler(lambda x: x.data == 'lp3')
async def lp1(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text="#3 — Октябрьский округ, Липецк")
    await bot.send_location(callback_query.from_user.id, 52.570931, 39.515099)
    await bot.send_message(callback_query.from_user.id, text="Всего мест - 30\nСвободных мест - ...",
                           reply_markup=kb.lp_book)


@dp.callback_query_handler(lambda x: x.data == 'lp4')
async def lp1(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text="#4 — Косырёвское кладбище, Липецк")
    await bot.send_location(callback_query.from_user.id, 52.609416, 39.435528)
    await bot.send_message(callback_query.from_user.id, text="Всего мест - 30\nСвободных мест - ...",
                           reply_markup=kb.lp_book)


@dp.callback_query_handler(lambda x: x.data == 'lp5')
async def lp1(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text="#5 — Старый Студеновский карьер, Липецк")
    await bot.send_location(callback_query.from_user.id, 52.644667, 39.617297)
    await bot.send_message(callback_query.from_user.id, text="Всего мест - 30\nСвободных мест - ...",
                           reply_markup=kb.lp_book)


@dp.callback_query_handler(lambda x: x.data == 'lp_book')
async def lp1_book(callback_query: types.CallbackQuery):
    if db.book_parking(callback_query.from_user.id) == "Мало денег":
        await bot.send_message(callback_query.from_user.id, text="У вас недостаточно денег")
    else:
        await bot.send_photo(callback_query.from_user.id,
                             photo=make_qrcode("https://jienivets.github.io/FanovParkingServices/pages/parcing.html"),
                             has_spoiler=True)
        await bot.send_message(callback_query.from_user.id, text="Предъявите QR код при въезде")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
