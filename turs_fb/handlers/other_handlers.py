from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const



from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import FSMFillForm

from lexicon.lexicon_ru import LEXICON_RU

router = Router()


async def go_clicked(callback: CallbackQuery, button: Button,
                     manager: DialogManager):
  await callback.message.answer("Going on!")

@router.message(F.text == 'диалог')
async def dialog_process_command(message: Message,
                                 #callback: CallbackQuery,
                                 button: Button,
                                 manager: DialogManager
                                 ):
  await message.answer(text='ответ на диалог')
  go_btn = Button(
  	Const("Go"),
    id="go",  # id is used to detect which button is clicked
    on_click=go_clicked,
  )


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message(StateFilter(default_state))
async def send_answer(message: Message):
  await message.reply(text=LEXICON_RU['other_answer'])