from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from db import Database
from io import BytesIO
from datetime import date
import logging
import config
import keyboard as kb
import qrcode

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)

db = Database('park_db.db')


class AllStates(StatesGroup):
    waiting_for_support = State()


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


@dp.callback_query_handler(lambda x: x.data[:2] == 'lp')
async def lp(callback_query: types.CallbackQuery):
    callback = callback_query.data
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text=db.get_name_park(callback))
    await bot.send_location(callback_query.from_user.id, db.get_lat(callback), db.get_lon(callback))
    await bot.send_message(callback_query.from_user.id,
                           text=f"Всего мест - {db.get_mest(callback)}\nСвободных мест - {db.get_sv_mest(callback)}",
                           reply_markup=kb.book)


@dp.callback_query_handler(lambda x: x.data == 'book')
async def booking_car(callback_query: types.CallbackQuery):
    await AllStates.waiting_for_support.set()
    await bot.send_message(callback_query.from_user.id, text="Укажите номер  автомобиля, пример - о001оо777")


@dp.message_handler(state=AllStates.waiting_for_support)
async def check_booking(message: types.Message, state: FSMContext):
    mes = message.text
    if mes[0].isalpha() and mes[1:4].isalnum() and mes[4:6].isalpha() and mes[6:].isalnum():
        if db.book_parking(message.from_user.id) == "Мало денег":
            await bot.send_message(message.from_user.id, text="У вас недостаточно денег")
        else:
            db.set_car_number(message.from_user.id, mes)
            await bot.send_photo(message.from_user.id,
                                 photo=make_qrcode(f"{mes}{message.from_user.id}"),
                                 has_spoiler=True)
            await bot.send_message(message.from_user.id, text="Предъявите QR код при въезде")
            await state.finish()
    else:
        await message.answer("Вы указали неправильный номер машины, отправьте ещё раз, пример - о001оо777")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
