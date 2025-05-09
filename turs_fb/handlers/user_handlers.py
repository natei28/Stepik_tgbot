from aiogram import F, Router

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
from config_data.config import user_dict, FSMFillForm
from aiogram.filters import Command, CommandStart, StateFilter
#from keyboards.keyboards import game_kb, yes_no_kb
from lexicon.lexicon_ru import LEXICON_RU

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
  await state.set_state(FSMFillForm.fill_name)
  
  
#router.message.register(process_start_command, Command(commands="start"), StateFilter(default_state))