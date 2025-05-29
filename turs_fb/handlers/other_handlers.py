from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const



from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import FSMFillForm, user_chek_fruit

from lexicon.lexicon_ru import LEXICON_RU, FRUIT_LIST, FRUIT_LIST_BASE
from keyboards.keyboards import check_fruit_modkb

#from services.services import check_fruit_modkb


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

@router.message(StateFilter(default_state), F.text == 'Фрукты')
async def process_fruit_list(message: Message, state: FSMContext):
  fruits_markup = check_fruit_modkb(FRUIT_LIST)
  await message.answer(text='Выбирете фрукты',
                       reply_markup=fruits_markup)
  await state.set_state(FSMFillForm.check_fruit)

#@router.callback_query(StateFilter(FSMFillForm.check_fruit), F.data.in_(['check_aple', 'check_orange', 'check_banan', 'check_kiwi']))
@router.callback_query(StateFilter(FSMFillForm.check_fruit), F.data.in_(list(FRUIT_LIST_BASE.keys())))
async def process_check_fruit(callback: CallbackQuery, state: FSMContext):
  if FRUIT_LIST_BASE[callback.data] in (user_chek_fruit):
    FRUIT_LIST[callback.data] = FRUIT_LIST_BASE[callback.data]
    user_chek_fruit.remove(FRUIT_LIST_BASE[callback.data])
    print(f'Пользователь выбрал:{user_chek_fruit}')
  else:
    FRUIT_LIST[callback.data] = f" ✔️ {FRUIT_LIST_BASE[callback.data]}"
    user_chek_fruit.append(FRUIT_LIST_BASE[callback.data])
    print(FRUIT_LIST[callback.data])
    print(f'Пользователь выбрал:{user_chek_fruit}')
  
  fruits_markup = check_fruit_modkb(FRUIT_LIST)
  await callback.message.edit_text(text=('Выбирете фрукты, один или несколько'),
                         reply_markup=fruits_markup)
# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message(StateFilter(default_state))
async def send_answer(message: Message):
  await message.reply(text=LEXICON_RU['other_answer'])