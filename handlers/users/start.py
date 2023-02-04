import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart(),state="*")
async def bot_start(message: types.Message,state: FSMContext):
    await state.finish()
    name = message.from_user.full_name
    # Foydalanuvchini bazaga qo'shamiz
    try:
        db.add_user(id=message.from_user.id,
                    name=name)
        await message.answer(f"Botimizga xush kelibsiz {name}\nBotni yangilayabmiz hozircha bot ishlamaydi bot ishga tushganda o'zimiz xabar beramiz etiboringgiz uchun raxmat 😊")
        # Adminga xabar beramiz
        count = db.count_users()[0]
        msg = f"Bazaga yangi user qo'shildi\n🙎🏻‍♂️ Name: <b>{message.from_user.full_name}</b>\n🆔 ID si: <code>{message.from_user.id}</code>\n✉️ Username: @{message.from_user.username}\n\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=ADMINS[0], text=f"🙎🏻‍♂️ <b>{name}</b> bazaga oldin qo'shilgan\n✉️ Username: @{message.from_user.username}\n🆔 ID si: <code>{message.from_user.id}</code>")
        await message.answer(f"Botimizga xush kelibsiz {name}\nBotni yangilayabmiz hozircha bot ishlamaydi bot ishga tushganda o'zimiz xabar beramiz etiboringgiz uchun raxmat 😊")
