from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
import random

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const



BOT_TOKEN = '7437970301:AAHv2laK19z9pyghAP5MPRQDozhcrDifP7c'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def go_clicked(callback: CallbackQuery, button: Button,
                     manager: DialogManager):
    await callback.message.answer("Going on!")


go_btn = Button(
    Const("Go"),
    id="go",  # id is used to detect which button is clicked
    on_click=go_clicked,
)



if __name__ == '__main__':
  dp.run_polling(bot)