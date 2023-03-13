from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import random
import sqlite3
from datetime import datetime

from config import TOKEN
from kb import *

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

bd = sqlite3.connect('database.db')
cursor = bd.cursor()


class Form(StatesGroup):
    gesture = State()
    bank = State()
    get_credit = State()

items = {
    "✊": "✌️",
    "✌️": "✋",
    "✋": "✊"
}

list = list(items.keys())


@dp.message_handler(commands=["self_photo"])
async def user_photo(message):
    photo = await bot.get_user_profile_photos(user_id=1344795663)
    await bot.send_photo(message.chat.id, photo.photos[0][2].file_id)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    usern = message.from_user.username
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {usern}(
        cash INT,
        diamond INT,
        count1 INT,
        count2 INT,
        count3 INT,
        count4 INT,
        achi1 TEXT,
        achi2 TEXT,
        achi3 TEXT,
        achi4 TEXT,
        credit INT,
        count_credit INT,
        date INT
    )""")
    bd.commit()
    
    cursor.execute(f"SELECT * FROM {usern}")
    fetc = cursor.fetchall()
    
    if len(fetc) == 0:
        cursor.execute(f"""INSERT INTO {usern}(
                cash,
                diamond,
                count1,
                count2,
                count3,
                count4,
                achi1,
                achi2,
                achi3,
                achi4,
                credit,
                count_credit,
                date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (200,
                0,
                0,
                0,
                0,
                0,
                "не виконанно",
                "не виконанно",
                "не виконанно",
                "не виконанно",
                0,
                0,
                0,)
            )
        bd.commit()
        
    cursor.execute(f"SELECT * FROM {usern}")
    fetc = cursor.fetchall()

    await bot.send_message(message.from_user.id, f"Вас вітатає гра \"Камінь Ножиці Папір\"")
    await bot.send_message(message.from_user.id, f"Ваш баланс:\n{fetc[0][0]}💵\n{fetc[0][1]}💎", reply_markup=men)


@dp.message_handler()
async def game_menu(message: types.Message):
    cursor.execute(f"SELECT * FROM {message.from_user.username}")
    fetch = cursor.fetchall()
    dt = datetime.now()

    def update_progress():
        """Оновляємо прогрес гравця"""
        global achi1, achi2, achi3, achi4
        global count1, count2, count3, count4
        global cash, diamond

        usern = message.from_user.username
        cursor.execute(f"SELECT * FROM {usern}")
        fetc = cursor.fetchall()
        
        cash = fetc[0][0]
        diamond = fetc[0][1]
        
        achi1 = fetc[0][6]
        achi2 = fetc[0][7]
        achi3 = fetc[0][8]
        achi4 = fetc[0][9]
        
        count1 = fetc[0][2]
        count2 = fetc[0][3]
        count3 = fetc[0][4]
        count4 = fetc[0][5]

    def update_achi():
        """Оновлюємо значення досягнень"""
        global achi1, achi2, achi3, achi4
        global diamond
        global count1, count2, count3, count4
        
        if cash >= 500 and count4 == 0:
            cursor.execute(f"UPDATE {message.from_user.username} SET achi4 == 'виконанно'")
            cursor.execute(f"UPDATE {message.from_user.username} SET count4 == 1")
            cursor.execute(f"UPDATE {message.from_user.username} SET diamond == diamond + 5")
            bd.commit()
        elif cash < 500 and count4 == 1:
            cursor.execute(f"UPDATE {message.from_user.username} SET achi4 == 'не виконанно'")
            cursor.execute(f"UPDATE {message.from_user.username} SET count4 == 0")
            cursor.execute(f"UPDATE {message.from_user.username} SET diamond == diamond - 5")
            bd.commit()
            
        if cash >= 750 and count3 == 0:
            cursor.execute(f"UPDATE {message.from_user.username} SET achi3 == 'виконанно'")
            cursor.execute(f"UPDATE {message.from_user.username} SET count3 == 1")
            cursor.execute(f"UPDATE {message.from_user.username} SET diamond == diamond + 10")
            bd.commit()
        elif cash < 750 and count3 == 1:
            cursor.execute(f"UPDATE {message.from_user.username} SET achi3 == 'не виконанно'")
            cursor.execute(f"UPDATE {message.from_user.username} SET count3 == 0")
            cursor.execute(f"UPDATE {message.from_user.username} SET diamond == diamond - 10")
            bd.commit()
            
        if cash >= 1000 and count2 == 0:
            cursor.execute(f"UPDATE {message.from_user.username} SET achi2 == 'виконанно'")
            cursor.execute(f"UPDATE {message.from_user.username} SET count2 == 1")
            cursor.execute(f"UPDATE {message.from_user.username} SET diamond == diamond + 20")
            bd.commit()
        elif cash < 1000 and count2 == 1:
            cursor.execute(f"UPDATE {message.from_user.username} SET achi2 == 'не виконанно'")
            cursor.execute(f"UPDATE {message.from_user.username} SET count2 == 0")
            cursor.execute(f"UPDATE {message.from_user.username} SET diamond == diamond - 20")
            bd.commit()
            
        if cash >= 1500 and count1 == 0:
            cursor.execute(f"UPDATE {message.from_user.username} SET achi1 == 'виконанно'")
            cursor.execute(f"UPDATE {message.from_user.username} SET count1 == 1")
            cursor.execute(f"UPDATE {message.from_user.username} SET diamond == diamond + 50")
            bd.commit()
        elif cash < 1500 and count1 == 1:
            cursor.execute(f"UPDATE {message.from_user.username} SET achi1 == 'не виконанно'")
            cursor.execute(f"UPDATE {message.from_user.username} SET count1 == 0")
            cursor.execute(f"UPDATE {message.from_user.username} SET diamond == diamond - 50")
            bd.commit()


    if fetch[0][12] != 0 and fetch[0][12] != dt.day:
        credit = fetch[0][10]
        credit = credit / 4
        await bot.send_message(message.from_user.id, f"З вашого рахунку боло знято вітсоткі по кредиту: \
{credit}💵\n\nБуть ласка виплатіть кредит😊:\nВаша заборгованість: {fetch[0][10]}💵")
        cursor.execute(f"UPDATE {message.from_user.username} SET cash == cash - {credit}")
        cursor.execute(f"UPDATE {message.from_user.username} SET date == {dt.day}")


    update_progress()
    update_achi()


    if message.text == "Грати на 50💵" and cash >= 50:
        await Form.gesture.set()
        await bot.send_message(message.from_user.id, "Виберіть жест:", reply_markup=button)
        
    elif message.text == "Грати на 50💵" and cash < 50:
        await bot.send_message(message.from_user.id, "Вибачте у вас не вистачає грошей😢")
        
    elif message.text == "Не грати більше":
        await bot.send_message(message.from_user.id, "Меню:", reply_markup=men)
        
    elif message.text == "Баланс💳":
        update_progress()
        update_achi()
        await bot.send_message(message.from_user.id, f"Ваш баланс:\n{cash}💵\n{diamond}💎")

    elif message.text == "Досягнення📈":
        update_progress()
        update_achi()
        await bot.send_message(message.from_user.id, f"🏆Заробити 1500💵 - {achi1} +50💎\n\
🥇Заробити 1000💵 - {achi2} +20💎\n🥈Заробити 750💵 - {achi3} +10💎\n\
🥉Заробити 500💵 - {achi4} +5💎")

    elif message.text == "💸Екстра гроші💵" and fetch[0][11] == 1 and fetch[0][0] <= 50:
        cursor.execute(f"UPDATE {message.from_user.username} SET cash = 100")
        bd.commit()
        await bot.send_message(message.from_user.id, "Функція 💸Екстра гроші💵 допоможе у критичній ситуації😅")

    elif message.text == "💸Екстра гроші💵" and fetch[0][0] > 50:
        await bot.send_message(message.from_user.id, """Функція 💸Екстра гроші💵 дає вам 2-й шанс.

Як це працює?
Коли на вашому балансі немає жодної копійки та ви взили кредит ця функція дасть вам стільки 💵 скільки потрібно, \
щоб на балансі було 100💵""")

    elif message.text == "Банк🏦":
        usern = message.from_user.username
        cursor.execute(f"SELECT * FROM {usern}")
        fetc = cursor.fetchall()

        await Form.bank.set()
        await bot.send_message(message.from_user.id, "У банку🏦 ви можете взяти кредит, \
але якщо ви не віддасте заборгованість до настання наступної доби(до 00:00) у вас буде знято 25% 💵 які ви заборгували",
                             reply_markup=bank_b)
        
        await bot.send_message(message.from_user.id, f"Ваша заборгованість:\n{fetc[0][10]}💵")

    elif message.text == "Правила📒":
        await bot.send_message(message.from_user.id, """Якій жест чому відповідає:
✌️ - ножиці
✋ - папір
✊ - камінь

Гра камінь ножниці папір дуже проста.
Якщо ✌️ проти ✋, то ножиці ріжуть папір.
Якщо ✋ проти ✊, то папір накриває камінь.
Якщо ✊ проти ✌️, то камінь перебивиє ножиці.

У тільки цьому боті ви можете взяти та погасити його
""")

    else:
        await bot.send_message(message.from_user.id, "Вибачте але я вас не розумію😞", reply_markup=men)


@dp.message_handler(state=Form.gesture)
async def process_game(message: types.Message, state: FSMContext):
    def update_balance():
        """Оновляємо баланс гравця"""
        global cash
        
        usern = message.from_user.username
        cursor.execute(f"SELECT * FROM {usern}")
        fetc = cursor.fetchall()
        
        cash = fetc[0][0]
    
    rand = random.choice(list)
    user = message.text

    if user == "🖕":
        await bot.send_message(message.from_user.id, f"Переможець: {message.from_user.first_name} +50💵\n\
Проти фака немає знака😎")
        
        cursor.execute(f"UPDATE {message.from_user.username} SET cash == cash + 50")
        bd.commit()
        
        update_balance()
        
        await bot.send_message(message.from_user.id, f"БОТ : {rand}\n\
{message.from_user.first_name} : {message.text}\n\nВаш баланс:\n{cash}💵")
        await bot.send_message(message.from_user.id, "Бажаєте зіграти на 50💵 ще раз?", reply_markup=menu_but)
        await state.finish()

    elif rand == user:
        await bot.send_message(message.from_user.id, "Нічія\nПродовжуємо грати")
        await bot.send_message(message.from_user.id, f"БОТ : {rand}\n\
{message.from_user.first_name} : {message.text}\n\nВаш баланс:\n{cash}💵")

    for i, j in items.items():
        if rand == i and user == j:
            await bot.send_message(message.from_user.id, "Переможець: БОТ +50💵")
            
            cursor.execute(f"UPDATE {message.from_user.username} SET cash == cash - 50")
            bd.commit()
        
            update_balance()
            
            await bot.send_message(message.from_user.id, f"БОТ : {rand}\n\
{message.from_user.first_name} : {message.text}\n\nВаш баланс:\n{cash}💵")
            await bot.send_message(message.from_user.id, "Бажаєте зіграти на 50💵 ще раз?", reply_markup=menu_but)
            await state.finish()
            break
        
        elif user == i and rand == j:
            await bot.send_message(message.from_user.id, f"Переможець: {message.from_user.first_name} +50💵")
            
            cursor.execute(f"UPDATE {message.from_user.username} SET cash == cash + 50")
            bd.commit()
        
            update_balance()
            
            await bot.send_message(message.from_user.id, f"БОТ : {rand}\n\
{message.from_user.first_name} : {message.text}\n\nВаш баланс:\n{cash}💵")
            await bot.send_message(message.from_user.id, "Бажаєте зіграти на 50💵 ще раз?", reply_markup=menu_but)
            await state.finish()
            break


@dp.message_handler(state=Form.bank)
async def bank_menu(message: types.Message, state: FSMContext):
    usern = message.from_user.username
    cursor.execute(f"SELECT * FROM {usern}")
    fetc = cursor.fetchall()


    if message.text == "Взяти кредит💰" and fetc[0][11] != 1:
        await bot.send_message(message.from_user.id, "Введіть суму 💵 на яку ви хочете взяти кредит",
                               reply_markup=credit_b)
        await Form.get_credit.set()
    
    elif message.text == "Взяти кредит💰" and fetc[0][11] == 1:
        await bot.send_message(message.from_user.id, "Спершу погасіть кредит щоб взяти новий😊")
        
    if message.text == "Віддати кредит💰" and fetc[0][11] == 1 and fetc[0][10] <= cash:
        await bot.send_message(message.from_user.id, "Кредит погашно😊")
        cursor.execute(f"UPDATE {message.from_user.username} SET credit == 0")
        cursor.execute(f"UPDATE {message.from_user.username} SET cash == cash - {fetc[0][10]}")
        cursor.execute(f"UPDATE {message.from_user.username} SET count_credit == 0")
        cursor.execute(f"UPDATE {message.from_user.username} SET date == 0")
        bd.commit()
    
    elif message.text == "Віддати кредит💰" and fetc[0][11] == 1 and fetc[0][10] > cash:
        await bot.send_message(message.from_user.id, "Вибачте але у вас не вистачає грошей щоб погасити заборгованість😞")
        await bot.send_message(message.from_user.id, f"Ваша заборгованість:\n{fetc[0][10]}💵")
        

    elif message.text == "Віддати кредит💰" and fetc[0][11] == 0:
        await bot.send_message(message.from_user.id, "У вас не має кредиту👍")
        

    if message.text == "Назад⬅️":
        await bot.send_message(message.from_user.id, "Меню:", reply_markup=men)
        await state.finish()


@dp.message_handler(state=Form.get_credit)
async def bank_menu(message: types.Message, state: FSMContext):
    if message.text != "Назад⬅️":
        dt = datetime.now()
        cursor.execute(f"UPDATE {message.from_user.username} SET credit == {message.text}")
        cursor.execute(f"UPDATE {message.from_user.username} SET cash == cash + {message.text}")
        cursor.execute(f"UPDATE {message.from_user.username} SET count_credit == 1")
        cursor.execute(f"UPDATE {message.from_user.username} SET date == {dt.day}")
        bd.commit()

        cursor.execute(f"SELECT * FROM {message.from_user.username}")
        fetc = cursor.fetchall()

        await bot.send_message(message.from_user.id, "Кредит взято", reply_markup=bank_b)
        await bot.send_message(message.from_user.id, f"Ваша заборгованість:\n{fetc[0][10]}💵")

        await state.finish()
        await Form.bank.set()
    else:
        await bot.send_message(message.from_user.id, "Кредит - це зло😅", reply_markup=bank_b)
        await state.finish()
        await Form.bank.set()

if __name__ == '__main__':
    executor.start_polling(dp)
