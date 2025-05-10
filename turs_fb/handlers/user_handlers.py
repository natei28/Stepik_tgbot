import asyncio
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
from aiogram.filters import Command, CommandStart, StateFilter

from keyboards.keyboards import markup_gender
from lexicon.lexicon_ru import LEXICON_RU
from config_data.config import user_dict, FSMFillForm

router = Router()

# Этот зэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команлу /fillform
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
  await message.answer(text=LEXICON_RU['/start'])

# Этот хэндлер будет срабатывать на комманду /cancel
# в состоянии по умолчанию и сообщать, что это команда
# работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
  await message.answer(text=LEXICON_RU['/cancel_outFSM'])

# Этот хэндлер будет срабатывать на команду /cancel
# в любом состоянию кроме состояния по умолчанию и 
# отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_inState_command(message: Message, state: FSMContext):
  await message.answer(text=LEXICON_RU['/cancel_inFSM'])
  await state.clear()
  

# Этот хэндлер будет срабатывать на команду /fillform
# и переврдить бота в состояние одидания ввода Имени
@router.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
  await message.answer(text=LEXICON_RU['/fillform'])
  await asyncio.sleep(1) 
  await message.answer(text=LEXICON_RU['name_sent'])
  await state.set_state(FSMFillForm.fill_name)
  
  
# Этот хэндлер будет срабатывать если введено корректное Имя
# и переводить бота в состочние ожидания ввода возраста
@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
  # Сохраняем введенное имя в хранилище по ключу name
  await state.update_data(name=message.text)
  await message.answer(text=LEXICON_RU['thanks'])
  await asyncio.sleep(1) 
  await message.answer(text=LEXICON_RU['age_sent'])
  await state.set_state(FSMFillForm.fill_age)
  
# Этот хэндлер будет срабатывать,если во время ввода
# имени введено чтото некоректное
@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
  await message.answer(text=LEXICON_RU['wrong'])
  await asyncio.sleep(1) 
  await message.answer(text=LEXICON_RU['note_name'])


# Этот хэндлер будет срабатывать, если введен коректный возраст
# и переводить бота в состояние выбора пола
@router.message(StateFilter(FSMFillForm.fill_age),
                lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext):
  await state.update_data(age=message.text)
  await message.answer(text=LEXICON_RU['thanks'])
  await asyncio.sleep(1)
  await message.answer(text=LEXICON_RU['gender_sent'],
                       reply_markup=markup_gender)
  await state.set_state(FSMFillForm.fill_gender)
  
# Этот хэндлер будет сратавать, если во время ввода
# возраста ввести что нибудь некорректное
@router.message(StateFilter(FSMFillForm.fill_age))
async def warning_not_age(message: Message):
  await message.answer(text=LEXICON_RU['wrong'])
  await asyncio.sleep(1)
  await message.answer(text=LEXICON_RU['note_age'])




#router.message.register(process_start_command, Command(commands="start"), StateFilter(default_state))