import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from aiogram.dispatcher.filters.state import StatesGroup, State
from states.state import Reklama
from aiogram.dispatcher import FSMContext

@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[0])
        name.append(user[1])
    data = {"ID" : id,"Name": name}
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)
       
@dp.message_handler(text="/reklama", user_id=ADMINS, state="*")
async def optional_ad(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Menga reklama uchun ixtiyoriy xabar jo'nating va men uni foydalanuvchilarga jo'nataman.")
    await Reklama.optional_reklama.set()

@dp.message_handler(state=Reklama.optional_reklama)
async def send_optional_ad(message: types.Message, state: FSMContext):
    users = db.select_all_users()
    try:
        for user in users:
            user_id = user[0]
            try:
                await message.send_copy(chat_id=user_id)
                await asyncio.sleep(0.05)
            except:
                pass
    except Exception as error:
        print(error)
    finally:
        await message.answer(text="Reklama foydalanuvchilarga jo'natildi")
    await state.finish()
# @dp.message_handler(text="/reklama", user_id=ADMINS)
# async def send_ad_to_all(message: types.Message):
#     users = db.select_all_users()
#     for user in users:
#         user_id = user[0]
#         try:
#             await bot.send_message(chat_id=user_id, text="<b>Bot ishga tushdi /start bosib ishlatishingiz mumkin 😊</b>",parse_mode='HTML')
#             await asyncio.sleep(0.05)
#         except Exception:
#             await message.answer(f"<b>{user[1]}</b> botni bloklagani uchun unga xabar bormadi 😭")


@dp.message_handler(text="/count",user_id = ADMINS)
async def count(message: types.Message):
    user_count = db.count_users()[0]
    await message.answer(f"Bazada <b>{user_count}</b> da foydalanuvchi bor")

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")
