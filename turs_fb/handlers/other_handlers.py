import sys
import locale
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import StateFilter, or_f
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, get_user_locale

from config_data.config import FSMFillForm, user_chek_fruit
from lexicon.lexicon_ru import LEXICON_RU, FRUIT_LIST
from keyboards.keyboards import create_inline_kb

router = Router()

@router.message(StateFilter(default_state), F.text == 'Фрукты')
async def process_fruit_list(message: Message, state: FSMContext):
  #fruits_markup = check_fruit_modkb(FRUIT_LIST)
  fruits_markup = create_inline_kb(3, FRUIT_LIST)
  await message.answer(text='Выбирете фрукты',
                       reply_markup=fruits_markup)
  await state.set_state(FSMFillForm.check_fruit)


#@router.callback_query(StateFilter(FSMFillForm.check_fruit), F.data.in_(['check_aple', 'check_orange', 'check_banan', 'check_kiwi']))
@router.callback_query(StateFilter(FSMFillForm.check_fruit), F.data.in_(list(FRUIT_LIST.keys())))
async def process_check_fruit(callback: CallbackQuery, state: FSMContext):
  if FRUIT_LIST[callback.data] in (user_chek_fruit):
    #FRUIT_LIST_MOD[callback.data] = FRUIT_LIST[callback.data]
    FRUIT_LIST[callback.data] = FRUIT_LIST[callback.data][4:]
    #user_chek_fruit.remove(FRUIT_LIST[callback.data])
    user_chek_fruit.remove(f" ✔️ {FRUIT_LIST[callback.data]}")
    print(f'Пользователь выбрал:{user_chek_fruit}')
  else:
    #FRUIT_LIST_MOD[callback.data] = f" ✔️ {FRUIT_LIST[callback.data]}"
    FRUIT_LIST[callback.data] = f" ✔️ {FRUIT_LIST[callback.data]}"
    user_chek_fruit.append(FRUIT_LIST[callback.data])
    print(f'Пользователь выбрал:{user_chek_fruit}')
  
  fruits_markup = create_inline_kb(3, FRUIT_LIST)
  await callback.message.edit_text(text=('Выбирете фрукты, один или несколько'),
                         reply_markup=fruits_markup)


# Хэндлер для вывода календаря
@router.message(F.text.lower() == 'календарь')
async def dialog_calendar(message: Message):
  await message.answer(text='Выбирете дату выезда',
                       reply_markup=await DialogCalendar(locale='ru_RU').start_calendar())

# dialog calendar usage
@router.callback_query(DialogCalendarCallback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
    selected, date = await DialogCalendar(locale='ru_RU').process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(f'Вы выбрали: {date.strftime("%d/%m/%Y")}')

@router.message(or_f(F.text == 'Ком3', F.text == 'Ком4'))
@router.message((F.text == 'Ком5') | (F.text == 'Ком6'))
async def test_fun(message: Message):
  await message.reply(message.text)


# Хэндлер для сообщений, которые не попали в другие хэндлеры
#@router.message(StateFilter(default_state))
#async def send_answer(message: Message):
#  await message.reply(text=LEXICON_RU['other_answer'])