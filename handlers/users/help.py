from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from aiogram.dispatcher import FSMContext

@dp.message_handler(CommandHelp(),state="*")
async def bot_help(message: types.Message,state="*"):
        await state.finish()
        text = ("Buyruqlar: ",
                "/start - Botni ishga tushirish",
                "/help - Yordam",
                "Admin: @azikk_0418")

        await message.answer("\n".join(text))
