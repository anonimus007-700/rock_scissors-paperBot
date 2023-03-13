from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

back_b = KeyboardButton('Назад⬅️')

but1 = KeyboardButton('✊')
but2 = KeyboardButton('✌️')
but3 = KeyboardButton('✋')
button = ReplyKeyboardMarkup(resize_keyboard=True).add(but1, but2, but3)

menu_but1 = KeyboardButton('Грати на 50💵')
menu_but2 = KeyboardButton('Не грати більше')
menu_but = ReplyKeyboardMarkup(resize_keyboard=True).add(menu_but1, menu_but2)

men1 = KeyboardButton('Грати на 50💵')
men2 = KeyboardButton('Баланс💳')
men3 = KeyboardButton('Досягнення📈')
men4 = KeyboardButton('Банк🏦')
men5 = KeyboardButton('Правила📒')
men6 = KeyboardButton('💸Екстра гроші💵')
men = ReplyKeyboardMarkup(resize_keyboard=True).row(men1, men2, men3).add(men4, men5).row(men6)

bank_b1 = KeyboardButton('Взяти кредит💰')
bank_b2 = KeyboardButton('Віддати кредит💰')
bank_b = ReplyKeyboardMarkup(resize_keyboard=True).row(bank_b1, bank_b2).add(back_b)

credit_b1 = KeyboardButton(100)
credit_b2 = KeyboardButton(500)
credit_b2 = KeyboardButton(1000)
credit_b = ReplyKeyboardMarkup(resize_keyboard=True).row(credit_b1, credit_b2).add(back_b)
