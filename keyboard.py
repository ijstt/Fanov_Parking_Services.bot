from aiogram import types

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
profile_btn = types.KeyboardButton("Профиль👤")
booking_btn = types.KeyboardButton("Парковки🚗")
menu.add(booking_btn, profile_btn)

profile = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_btn = types.KeyboardButton("Назад⬅️")
help_btn = types.KeyboardButton("Обратиться в тех поддержку📱")
profile.add(help_btn, back_btn)

balance = types.InlineKeyboardMarkup(resize_keyboard=True)
balance_btn = types.InlineKeyboardButton("Пополнить баланс💰", callback_data='balance')
balance.add(balance_btn)

cities = types.InlineKeyboardMarkup(resize_keyboard=True)
lip = types.InlineKeyboardButton("Липецк", callback_data='lipetsk')
cities.add(lip)

lip_parks = types.InlineKeyboardMarkup(row_width=3)
back = types.ReplyKeyboardMarkup(resize_keyboard=True)
lip_park1 = types.InlineKeyboardButton("#1 — Коммунальная площадь, Липецк", callback_data='lp1')
lip_park2 = types.InlineKeyboardButton("#2 — площадь Петра Великого, Липецк", callback_data='lp2')
lip_park3 = types.InlineKeyboardButton("#3 — Октябрьский округ, Липецк", callback_data='lp3')
lip_park4 = types.InlineKeyboardButton("#4 — Косырёвское кладбище, Липецк", callback_data='lp4')
lip_park5 = types.InlineKeyboardButton("#5 — Старый Студеновский карьер, Липецк", callback_data='lp5')
back_btn = types.KeyboardButton("Назад⬅️")
lip_parks.add(lip_park1, lip_park2, lip_park3, lip_park4, lip_park5)
back.add(back_btn)

lp_book = types.InlineKeyboardMarkup()
book = types.InlineKeyboardButton("Арендовать место", callback_data='lp_book')
lp_book.add(book)
